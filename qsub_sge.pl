#!/share/nas2/genome/biosoft/perl/current/bin/perl

=head1 Name

qsub-sge.pl -- control processes running on linux SGE system

=head1 Description

=head1 Version

=head1 Usage
  
  perl qsub-sge.pl <jobs.txt>
  --queue <str>     specify the queue to use, default:cu
  --lines <num>     set number of lines to form a job, default 1
  --interval <num>  set interval time of checking by qstat, default 15 seconds
  --maxproc <num>   set the maximum number of process in queue, default 10
  --secure <mark>   set the user defined job completition mark, can be any string
  --reqsub          reqsub the unfinished jobs untill they are finished.
  --resource <num>  per job need cpu,default:3
 

=head1 Exmple
  
  1.work with default options (the most simplest way)
  perl qsub-sge.pl ./work.sh

  2.work with user specifed options: (to select queue, set checking interval time, set number of lines in each job, and set number of maxmimun running jobs)
  perl qsub-sge.pl --queue cu -lines 3 --maxproc 10  ./work.sh

=cut


use strict;
use warnings;
use Getopt::Long;
use FindBin qw($Bin $Script);
use File::Basename qw(basename dirname); 
use Data::Dumper;

##get options from command line into variables and set default values
my ($Queue, $Interval, $Lines, $Maxproc, $Convert,$Secure,$Reqsub,$Resource,$Independent,$Old,$Verbose, $Help);
GetOptions(
	"lines:i"=>\$Lines,
	"maxproc:i"=>\$Maxproc,
	"interval:i"=>\$Interval,
	"queue:s"=>\$Queue,
	"convert:s"=>\$Convert,
	"secure:s"=>\$Secure,
	"reqsub"=>\$Reqsub,
	"resource:s"=>\$Resource,
	"independent"=>\$Independent,
	"Check:s"=>\$Old,
	"verbose"=>\$Verbose,
	"help"=>\$Help
);
$Queue ||= "cu";
$Interval ||= 15;
$Lines ||=1;
$Maxproc ||=10;
$Convert ||= 'no';
$Resource ||= 3;
$Old ||="yes";
if(defined $Independent)
{
	$Independent=1;
}
else
{
	$Independent=0;
}

die `pod2text $0` if (@ARGV == 0 || $Help);

my $work_shell_file = shift;

$Resource=~m/vf=(.+)G/;

##global variables
my $work_shell_file_globle = $work_shell_file.".$$.globle";
my $work_shell_file_error = $work_shell_file.".$$.error";
my $Work_dir = $work_shell_file.".$$.qsub";
my $current_dir = `pwd`; chomp $current_dir;

if ($Convert =~ /y/i) {
	absolute_path($work_shell_file,$work_shell_file_globle);
}else{
	$work_shell_file_globle = $work_shell_file;
}

my $work_shell_file_name=basename($work_shell_file);
if ($work_shell_file_name=~m/^\d+/) {
	print "The shell file name can not begin with a number !\n";
	exit;
}
$work_shell_file_name=~s/\.sh$//;
my $qstatname=$work_shell_file_name;
my @old_qsub=glob ("$work_shell_file.*.qsub");
chomp @old_qsub;
my @Shell;
if ($Old eq "no"|| @old_qsub<1) {
	foreach my $old (@old_qsub){
		my $error_file=$old;
		$error_file=~s/\.qsub$/\.error/;
		`rm -r $old` if(-d $old);
		`rm $error_file` if(-e $error_file);
	}

	## read from input file, make the qsub shell files
	my $line_mark = 0;
	my $Job_mark="00001";
	mkdir($Work_dir) if(!-d $Work_dir);
	$Work_dir=PATH($Work_dir);
	open IN, $work_shell_file_globle || die "fail open $work_shell_file_globle";
	my $jobsh;
	while(<IN>){
		chomp;
		next unless($_!~/^$/);
		if ($line_mark % $Lines == 0) {
			open OUT,">$Work_dir/$work_shell_file_name\_$Job_mark.sh" || die "failed creat $work_shell_file_name\_$Job_mark.sh";
			push @Shell,"$work_shell_file_name\_$Job_mark.sh";
			$jobsh="$Work_dir/$work_shell_file_name\_$Job_mark.sh";
			$Job_mark++;
		}
		s/\;\s*$//;
		if($_=~m/\&\&\s*$/){
			print OUT $_." echo This-Work-is-Completed! && touch $jobsh.Check\n" ;
		}else{
			print OUT $_."&& echo This-Work-is-Completed! && touch $jobsh.Check\n" ;
		}
		if ($line_mark % $Lines == $Lines - 1) {
			close OUT;
		}
		$line_mark++;
	}
	close IN;
	close OUT;
	print STDERR "make the qsub shell files done\n" if($Verbose);
}elsif($Old eq "yes" && @old_qsub!=0){
	my $last_qsub_time=0;my $last_qsub;
	if (@old_qsub>1) {
		for (my $i=0;$i<@old_qsub ;$i++) {
			my $time=(split/\./,$old_qsub[$i])[-2];
			if ($time>$last_qsub_time) {
				$last_qsub_time=$time;
				$last_qsub=$old_qsub[$i];
			}
		}
	}else{
		($last_qsub)=@old_qsub;
	}
	$Work_dir=PATH($last_qsub);
	my @old_shell=glob("$Work_dir/*.sh");
	foreach my $old_shell (sort @old_shell) {
		next if (-f "$old_shell.Check");
		push @Shell,$old_shell;
		my @error_file=glob("$old_shell.{e,o}*");
		`rm @error_file ` if(@error_file>0);
	}
	print "Check last time qsub have ",scalar@Shell," shell uncomplete.\n";
	print "That will continue the uncomplete jobs.\n";
}
my $qsub_cycle = 1;
while (@Shell)
{
	my %Alljob; ## store all the job IDs of this cycle
	my %Runjob; ## store the real running job IDs of this cycle
	my %Error;  ## store the unfinished jobs of this cycle
	chdir($Work_dir); ##enter into the qsub working directoy
	my $job_cmd = "qsub -V  -cwd -S /bin/sh  ";  ## -l h_vmem=16G,s_core=8 
	$job_cmd .= "-q $Queue "; ##set queue #Ming'an Sun 2009.03.30
        $job_cmd .= "-pe smp $Resource " ; ##set resource
	for (my $i=0; $i<@Shell; $i++) {
		while (1) {
			if ($i<3 || &queueJob() < $Maxproc) {
				my $jod_return = `$job_cmd $Shell[$i]`;
				my $job_id = $1 if($jod_return =~ /Your job (\d+)/);
				$Alljob{$job_id} = $Shell[$i];  ## job id => shell file name
				print STDERR "throw job $job_id in the $qsub_cycle cycle\n" if($Verbose);
				last;
			}else{
				print STDERR "wait for throwing next job in the $qsub_cycle cycle\n" if($Verbose);
				sleep $Interval ;
			}
		}
	}
	chdir($current_dir);
	while (1) {
		my $run_num = run_count(\%Alljob,\%Runjob);	
		last if($run_num == 0);
		print STDERR "There left $run_num jobs runing in the $qsub_cycle cycle\n" if(defined $Verbose);
		sleep $Interval;
	}

	print STDERR "All jobs finished, in the firt cycle in the $qsub_cycle cycle\n" if($Verbose);
	open OUT, ">>$work_shell_file_error" || die "fail create $$work_shell_file_error";
	chdir($Work_dir); ##enter into the qsub working directoy
	foreach my $job_id (sort keys %Alljob) {
		my $shell_file = $Alljob{$job_id};
		
		##read the .o file
		my $content;
		if (-f "$shell_file.o$job_id") {
			$content = `tail $shell_file.o$job_id `;
		}
		if ($content !~ /This-Work-is-Completed!/) {
			$Error{$job_id} = $shell_file;
			print OUT "In qsub cycle $qsub_cycle, In $shell_file.o$job_id,  \"This-Work-is-Completed!\" is not found, so this work may be unfinished\n";
		}
		##read the .e file
		if (-f "$shell_file.e$job_id")
		{
			$content = `tail $shell_file.e$job_id `;
		}
		##check the user defined job completion mark
		if (defined $Secure && $content !~ /$Secure/) {
			$Error{$job_id} = $shell_file;
			print OUT "In qsub cycle $qsub_cycle, In $shell_file.o$job_id,  \"$Secure\" is not found, so this work may be unfinished\n";
		}
	}
	@Shell = ();
	foreach my $job_id (sort keys %Error) {
		my $shell_file = $Error{$job_id};
		push @Shell,$shell_file;
	}
	
	$qsub_cycle++;
	if($qsub_cycle > 5){
		print OUT "\n\nProgram stopped because the reqsub cycle number has reached 5, the following jobs unfinished:\n";
		foreach my $job_id (sort keys %Error) {
			my $shell_file = $Error{$job_id};
			print OUT $shell_file."\n";
		}
		print OUT "Please check carefully for what errors happen, and redo the work, good luck!";
		die "\nProgram stopped because the reqsub cycle number has reached 5\n";
	}

	chdir($current_dir); ##return into original directory 
	close OUT;
	print STDERR "The secure mechanism is performed in the $qsub_cycle cycle\n" if($Verbose);

	last unless(defined $Reqsub);
}

print STDERR "\nqsub-sge.pl finished\n" if($Verbose);


####################################################
################### Sub Routines ###################
####################################################
sub PATH{
        my ($in)=@_;
        my $return="";
		my $cur_dir=`pwd`;chomp$cur_dir;
        if(-f $in)
        {
                my $dir=dirname($in);
                my $file=basename($in);
                chdir $dir;$dir=`pwd`;chomp $dir;
                $return="$dir/$file";
        }
        elsif(-d $in)
        {
                chdir $in;$return=`pwd`;chomp $return;
        }
        else
        {
                warn "Warning just for file and dir\n";
                exit;
        }
        chdir $cur_dir;
        return $return;
}

sub absolute_path
{
	my($in_file,$out_file)=@_;
	my($current_path,$shell_absolute_path);

	#get the current path ;
	$current_path=`pwd`;   
	chomp $current_path;

	#get the absolute path of the input shell file;
	if ($in_file=~/([^\/]+)$/){
		my $shell_local_path=$`;
		if ($in_file=~/^\//){
			$shell_absolute_path = $shell_local_path;		
		}else{
			$shell_absolute_path="$current_path"."/"."$shell_local_path";
		}
	}	
	
	open (IN,"$in_file");
	open (OUT,">$out_file");
	while (<IN>) {
	    chomp;
	    my @words=split /\s+/, $_;
		for (my $i=1; $i<@words; $i++)
		{
			if($words[$i] =~ /^(-.*)=(.*)$/)
			{
				my $paraName = $1;
				my $paraValue = $2;
				
				if ($paraValue !~ /\//) 
				{
					if (-f $paraValue || -d $paraValue) 
					{
						$paraValue = "./$paraValue";
					}
				}	
				$words[$i] = "$paraName\=$paraValue";			
			}
			else
			{
				if ($words[$i] !~ /\//) 
				{
					if (-f $words[$i] || -d $words[$i]) 
					{
						$words[$i] = "./$words[$i]";

					}elsif($words[$i-1] eq ">" || $words[$i-1] eq "2>")
					{
						$words[$i] = "./$words[$i]";
					}
				}
			}
		}

		for (my $i=0;$i<@words ;$i++)
		{
			if($words[$i] =~ /^(-.*)=(.*)$/)
			{
				my $paraName = $1;
				my $paraValue = $2;
				if ($paraValue !~ /\//) 
				{
					if (-f $paraValue || -d $paraValue) 
					{
						$paraValue = "$shell_absolute_path"."$paraValue";
					}
				}	
				$words[$i] = "$paraName\=$paraValue";
			}
			else
			{
				next if($words[$i]=~/\d?\>\//);
				if($words[$i]=~/(\d?\>)(\S+)/)
				{
					$words[$i]= $1."$shell_absolute_path"."$2";
				}
				elsif (($words[$i]!~/^\//) && ($words[$i]=~/\//)) 
				{
					$words[$i]= "$shell_absolute_path"."$words[$i]";
				}
			}
		}
		print OUT join("  ", @words), "\n";
	}
	close IN;
	close OUT;
}

sub run_count {
	my $all_p = shift;
	my $run_p = shift;
	my $run_num = 0;

	%$run_p = ();
	my $user = `whoami`; chomp $user;
          my $qstat_result = `qstat -u $user 2>&1`;
	if($qstat_result eq ""){
	    return $run_num;
	}elsif ($qstat_result !~ /job-ID/)
	{
		$run_num = -1;
		return $run_num;
	}else{
		my @jobs = split /\n/,$qstat_result; 
		foreach my $job_line (@jobs) {
			$job_line =~s/^\s+//;
			my @job_field = split /\s+/,$job_line;
			next if($job_field[3] ne $user);
			if (exists $all_p->{$job_field[0]}){
				
				my %died;
				died_nodes(\%died);
				my $node_name = $1 if($job_field[7] =~ /(compute-\d+-\d+)/);
				if (exists $died{$node_name}) {
					`qdel $job_field[0]`;
				}else{
					my $res=`qstat -j $job_field[0] 2>&1| grep job_name:|awk '{print $2}' `; 
					$run_p->{$job_field[0]} = $res;
					$run_num++;
				}
			}
		}
	}
	return $run_num;
}

## queue job number
sub queueJob{
	my $user = `whoami`; chomp $user;
	RE:
	my $qstat_result=`qstat -u $user 2>&1`;
	if($qstat_result eq ""){
		return 0;
	}elsif($qstat_result =~ /job-ID/){
		my @jobs = split("\n", $qstat_result);
		my $jobnum = @jobs-2;
		if($Independent==1){
			my $jobs=0;
			for (my $i=0;$i<@jobs ;$i++) {
				$jobs[$i]=~s/^\s+//;
				next if( $jobs[$i]=~/^[^\d]/);
				my $jobid=(split/\s+/,$jobs[$i])[0];
				my $jobname= `qstat -j $jobid 2>&1 | grep cwd:`;
				$jobname=(split/\s+/,$jobname)[1];
				$jobname=~s/_\d{5}\.sh$//;	
				$jobs++ if($jobname eq $Work_dir);
			}
			$jobnum=$jobs;
		}
		return $jobnum;
	}else{
		goto RE;
	}
}

sub died_nodes{
	my $died_p = shift;
	my @lines = split /\n/,`qhost`;
	shift @lines; shift @lines; shift @lines;  ##remove the first three title lines

	foreach  (@lines) {
		my @t = split /\s+/;
		my $node_name = $t[0];
		my $memory_use = $t[5];
		$died_p->{$node_name} = 1 if($memory_use eq '-');
	}
}
