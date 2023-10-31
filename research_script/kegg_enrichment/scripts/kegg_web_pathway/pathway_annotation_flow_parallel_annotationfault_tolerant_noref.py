# Embedded file name: pathway_annotation_flow_parallel_annotationfault_tolerant3.py
import sys
import os
import os.path
import urllib
import re
import argparse
from bs4 import BeautifulSoup as bs
from multiprocessing import Pool, cpu_count
from django.template import Template, Context, loader
from django.conf import settings
settings.configure(DEBUG=True, TEMPLATE_DEBUG=True, TEMPLATE_DIRS=(sys.path[0],))

skipp_patn  = re.compile(r'.*ko(01100|01110).*')
uncomplete_pathway_list = []
col_num = 0
def file_wash(filename):
    washed = []
    k = 0
    tmp = []
    for eachLine in open(filename):
        tmp.append(eachLine.strip())
    for line in tmp:
        if(line.startswith('#Term')):
            global col_num
            col_num = len(line.split("\t"))
            break
    for line in tmp:
        if line != '' and not line.startswith('#Term') and len(line.split('\t')) == col_num :
            washed.append(line.strip() + '\t' + str(k))
            k = k + 1
   
    return washed


def updown(file):
    up = {}
    down = {}
    deg_file = open(file).readlines()
    ## delete the first line, that is to say the header of the file
    head_line = deg_file.pop(0)
    assert head_line.strip() != ''
    headline_sep = head_line.split()
    for i, e in enumerate(headline_sep):
        if 'log2' in e.lower() and 'fold' in e.lower() and 'change' in e.lower():
            col = i
            break

    for eachLine in deg_file:
        if eachLine.strip() != '':
            temp = eachLine.split()
            ##for down DEG 
            if float(temp[col]) < 0:
                down[temp[0].strip()] = temp[col].strip()
            ##for up DEG
            else:
                up[temp[0].strip()] = temp[col].strip()

    return (up, down)
def read_html(abbr,pathway):
    filepath = "/allwegene/dat2/database/kegg_pathway_data/"+ abbr + "/" + pathway + ".html"
    file_object = open(filepath)
    all_the_text = file_object.read( )
    file_object.close( )
    return all_the_text

def copy_img(abbr,pathway,target_path):
    filepath = "/allwegene/dat2/database/kegg_pathway_data/" + abbr + "/" +  pathway + ".png"
    assert not os.system('cp ' + filepath + " " + target_path)
#skipp_term = ['ko01100','ko01110']
def main_flow(abbr,row):
    ##global is used to define global variable: col_num is column counts in the KEGG enrichment results file
    global col_num
    each = row.strip().split('\t')
    ## get pathway ID (each[2]), eg: osa00380
    pathway = each[2].strip().lower()
    ## get KEGG_ID/KO list  (each[8]), eg:osa:4331833|osa:4348531|
    ko = [ one_ko.strip() for one_ko in each[8].strip().split('|') ]
    ko_last = ko.pop(-1)
    assert ko_last == ''
    ## get input DEG IDs
    gene = [ one_gene.strip() for one_gene in each[7].strip().split('|') ]
    for col in range(7, col_num-1):
        temp = [ each_temp.strip() for each_temp in each[col].split('|') if each_temp.strip() != '' ]
        if list(set(temp)) == [] or list(set(temp)) == ['NA']:
            each[col] = 'NA'
        else:
            each[col] = ' '.join(temp)

    try:
        assert len(ko) == len(gene)
    except:
        print 'assert error' + pathway

    ko_gene = {}
    ko_red = []
    ko_yellow = []
    ko_green = []
    for i, each_ko in enumerate(ko):
        if each_ko != '':
            if each_ko not in ko_gene:
                ko_gene[each_ko] = {}
                ko_gene[each_ko]['up'] = []
                ko_gene[each_ko]['down'] = []
            if gene[i] in up:
                ko_gene[each_ko]['up'].append(gene[i])
            if gene[i] in down:
                ko_gene[each_ko]['down'].append(gene[i])

    try:
        content = read_html(abbr,pathway)
        soup = bs(content)
        copy_img(abbr,pathway,'src/')
        map = soup.map
        html_content = ""
        if pathway.endswith("01200") or pathway.endswith("01210") or pathway.endswith("01212") or pathway.endswith("01230") or pathway.endswith("01220") or pathway.endswith("01100"):
                for each_area in map.find_all('area'):
                    each_area['href'] = 'http://www.kegg.jp' + each_area['href']
                    #html_content += str(each_area.prettify(formatter=None))
        else:
    	    index = 0
            for each_area in map.find_all('area'):

                ko_set = [ each_ko.strip() for each_ko in re.search('\\?(.*)', each_area['href']).group(1).split('+') ]
                flag_red = 0
                flag_green = 0
                num = 0
                for each_ko in ko_set:
                    if each_ko in ko_gene:
                        if ko_gene[each_ko]['up'] != []:
                            flag_red = flag_red + 1
                            num = num + 1
                        if ko_gene[each_ko]['down'] != []:
                            flag_green = flag_green + 1
                            num = num + 1
                        
                img_src = ""
                if flag_red == num and num != 0:
                    img_src = "bg_red"
                if flag_green == num and num != 0:
                    img_src = "bg_green"
                if flag_green < num and flag_red < num:
                    img_src = "bg_yellow"

                each_area['href'] = 'http://www.kegg.jp' + each_area['href']
                #del each_area['onmouseout']
    	   
                if num != 0:
                    coords = each_area['coords'].split(",")
                    top = int(coords[1]) + 8
                    left = int(coords[0]) + 8
                    each_area['coords'] = "0,0,47,18"
                    html_content += "<div><span class='maps'><img class='maps' src='" + img_src + ".png' style='top:"+ str(top) +"px;left:"+ str(left) +"px;width:47px;height:18px;position:absolute;' usemap='#map_"+ str(index)  +"'>" + "<map name='map_"+ str(index) +"'>" + str(each_area.prettify(formatter=None)) + "</map></span> <span style='display:none;'>"
                    
                    inner_html = '<ul>'
                    for each_ko in ko_gene:
                        if each_ko in ko_set:
                            inner_html += '<li>%s</li>' % each_ko
                            if ko_gene[each_ko]['up'] != []:
                                inner_html += '<ul><li><font color=\"red\">Up regulated genes</font></li><ul><font color=\"red\">%s</font></ul></ul>' % ' '.join([ each_gene + '(' + up[each_gene] + ')' for each_gene in ko_gene[each_ko]['up'] ])
                            if ko_gene[each_ko]['down'] != []:
                                inner_html += '<ul><li><font color=\"green\">Down regulated genes</font></li><ul><font color=\"green\">%s</font></ul></ul>' % ' '.join([ each_gene + '(' + down[each_gene] + ')' for each_gene in ko_gene[each_ko]['down'] ])

                    inner_html += '</ul></span></div>'
                    html_content += inner_html
                index = index + 1

        t = loader.get_template('Kegg_map_template.html')
        c = Context({'title': pathway,'add_content':html_content,'map_content': str(map.prettify(formatter=None)),'image': pathway + '.png'})
        html = t.render(c)
        open('src/' + pathway + '.html', 'w').write(html)
        link = 'src/' + pathway + '.html'
        term = [link, each[0]] + each[3:-2] + [each[-1]]
    except:
        print pathway + ' detail map fail...'
        term = ['#', each[0]] + each[3:-2] + [each[-1]]

    return term


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='KEGG pathway enrichment web visualization for noref transcriptome kegg_web')
    parser.add_argument('--table', required=True, help='standard formated pathway enrichment input file')
    parser.add_argument('--diff', required=True, help='differential expression genes table generated from DEGseq or DEseq')
    parser.add_argument('--abbr', required=True, help='species abbr')
    argv = vars(parser.parse_args())
    filename = argv['table']
    DEG = argv['diff']
    abbr = argv['abbr']
    name = os.path.basename(filename)
    assert not os.system('cp -r %s .' % (sys.path[0] + '/src'))
    if not os.path.exists('src'):
        assert not os.system('mkdir src')
    parallel_result = []
    ##save kegg enrichment results into a list: row_pathway
    row_pathway = file_wash(filename)
    ## get UP/DOWN DEG id and the corresponding value of Log2FoldChange
    ## up and down are both dicts, the key is 'geneID', and the value is 'Log2FoldChange'
    up, down = updown(DEG)
    
    ## use cpu_count() to get the total cpu number of the current platform
    pool = Pool(processes=cpu_count())
    for eachrow in row_pathway:
        parallel_result.append(pool.apply_async(main_flow, (abbr,eachrow,)))

    pool.close()
    pool.join()
    
    result = [ '' for i in range(len(row_pathway)) ]
    for eachone in parallel_result:
        try:
            temp = eachone.get(timeout=10)
            result[int(temp[-1])] = temp[0:-1]
        except:
            uncomplete_pathway = row_pathway[parallel_result.index(eachone)]
            sys.stderr.write( '%s not complete W/I 10seconds' % uncomplete_pathway )
            if not re.match(skipp_patn, uncomplete_pathway):
                uncomplete_pathway_list.append(uncomplete_pathway)

    t = loader.get_template('Table_template.html')
    c = Context({'terms': result})
    html = t.render(c)
    open(name + '_rendered_html_detail.html', 'w').write(html)
if uncomplete_pathway_list:
    open('unfinished_pathway.txt','w').writelines(uncomplete_pathway_list)
   
