import sys
xml_file=sys.argv[1]
hsa_num=xml_file[0:8]

import xml.etree.ElementTree as ET
tree = ET.parse(xml_file)
root = tree.getroot()
import re

print tree
dict = {};
#allgenes = []
print root;
for child in root:
	print child.tag
	if (child.tag == "entry"):
		entryid = child.attrib['id'];
		if (child.attrib['type'] == "gene"):
			for grandchild in child:
				print grandchild.tag
				if (grandchild.tag == "graphics"):
					genelist = grandchild.attrib['name'].split(', '); 
					dict[entryid] = genelist;
		elif (child.attrib['type'] == "group"):
			allgenes = [];
			for grandchild in child:
				if (grandchild.tag == "component"):
					allgenes.append( grandchild.attrib['id'] );
			#print allgenes
			names = []
			for id in allgenes:
				#listlen = len(dict[str(id)])
				#print listlen
				names.append(dict[str(id)])
				print entryid, id, names
				dict[entryid] = names
				print dict[entryid]	
		
#for k in dict.keys():
#	print k, dict[k];

for relation in root.findall('relation'):
	reltype = relation.get('type')
	gene1 = dict[str(relation.get('entry1'))]
	gene2 = dict[str(relation.get('entry2'))]
#turn these lists into strings
	gene2str = ",".join(gene2)
	gene1str = ",".join(gene1)
	for subtype in relation.findall('subtype'):
		stype = subtype.get('name')	#interaction subtype
		if reltype == 'PPrel':	#just collect protein-protein interactions
           		if stype == 'activation':
	              		relation = (gene1str,'::',gene2str,'::True')
             			relation= "".join(relation)
                		#print relation
				#deap.write(joinedlist+'\n')
    			elif stype != 'activation':
              			relation = (gene1str,'::',gene2str,'::False')
      				relation  = "".join(relation)
				#print relation
                		#deap.write(joinedlist2+'\n')
			else:
   				None

entrynumberng=[]
entrynumber=[]
for entrynum in root.findall('entry'):
	if entrynum.get('type') != 'group':
        	entrynumberng.append(entrynum.get('id')+'\n')
	else:
        	entrynumber.append(entrynum.get('id')+'\n')

genelist=[]
for geneid in root.getiterator('graphics'):
    name = str(geneid.get('name'))
    name2 = name.split(",")
    if name2 != ['None']:
        genelist.append(name2[0]+'\n')
    else:
        None
       
entrynum_gene=[]
linenumber=0
for row in entrynumberng:
    row=row.strip('\n')
    entrynum_gene.append(row+'\t'+genelist[linenumber])
    linenumber +=1
    
d=[]
groupgenenames=[]
line3 = 1
total=0
for entry in root.findall('entry'):
    num_children = str(list(entry)[1:]).count('component')
    total = total+int(num_children)
    for component in entry.findall('component'):
        linenumber2 = component.get('id')
	gene_line = entrynum_gene[int(linenumber2)-1]
	gene_name = gene_line.split('\t')[1].strip()
        groupgenenames.append(gene_name)
    if num_children == 0:
       line3+=1
    else:
        d.append(str(line3)+'\t'+str(num_children))
        line3+=1

e=[]
for line in d:
    if total == 0:
        continue
    else:
        f=[]
        n=0 
        linenumberr=line.split('\t')[0]
        amount=line.split('\t')[1]
        entries=int(amount)-1
        group_genes = groupgenenames[0:int(amount)]
        groupgenenames=groupgenenames[int(amount):]
        while n<int(amount): 
            geness=group_genes[n]
            f.append(geness)
            n+=1
        e.append(f)
     
deap = open('deapformat_'+hsa_num,'w')
if total==0:
    cutoff=int(len(genelist))+1
else:
    cutoff=int(d[0].split('\t')[0])
Gm=[]
for relation in root.findall('relation'):
    reltype = relation.get('type')
    entry1 = (str(relation.get('entry1')))
    entry2 = (str(relation.get('entry2')))
    for subtype in relation.findall('subtype'):
        stype = subtype.get('name')
        if int(entry1)>=cutoff or int(entry2)>=cutoff:
            Gm.append(entry1+'\t'+entry2+'\t'+stype)
            continue
        else:
            None
        if reltype == 'PPrel':
            gene1=genelist[int(entry1)-1]
            gene2=genelist[int(entry2)-1]
            if stype == 'activation':
                list3 = (gene1.strip(),'::',gene2.strip(),'::True')
                joinedlist= "".join(list3)
		#print list3, joinedlist
                deap.write(joinedlist+'\n')
            else:
                list2 = (gene1.strip(),'::',gene2.strip(),'::False')
                joinedlist2 = "".join(list2)
                deap.write(joinedlist2+'\n')
        else:
            None



for line in Gm:
    if int(line.split('\t')[0]) >= cutoff and int(line.split('\t')[1]) < cutoff:
        number = int(line.split('\t')[0])-cutoff
        genedos=genelist[int(line.split('\t')[1])-1]
        typez=line.split('\t')[2]
        for value in range(int(d[number].split('\t')[1])):
            if typez == 'activation':
                list4 = (e[number][value].strip(),'::',genedos.strip(),'::True')
                joinedlist3= "".join(list4)
                deap.write(joinedlist3+'\n')
            else:
                list5 = (e[number][value].strip(),'::',genedos.strip(),'::False')
                joinedlist4 = "".join(list5)
                deap.write(joinedlist4+'\n')
    if int(line.split('\t')[1]) >= cutoff and int(line.split('\t')[0]) < cutoff:
        number2 = int(line.split('\t')[1])-cutoff
        geneuno=genelist[int(line.split('\t')[0])-1]
        typezz=line.split('\t')[2]
        for valuez in range(int(d[number2].split('\t')[1])):
            if typezz=='activation':
                list6 = (geneuno.strip(),'::',e[number2][valuez].strip(),'::True')
                joinedlist6="".join(list6)
                deap.write(joinedlist6+'\n')
            else:
                list7 = (geneuno.strip(),'::',e[number2][valuez].strip(),'::False')
                joinedlist7="".join(list7)
                deap.write(joinedlist7+'\n')
    if int(line.split('\t')[1]) >= cutoff and int(line.split('\t')[0]) >= cutoff:
        number3 = int(line.split('\t')[0])-cutoff
        number4 = int(line.split('\t')[1])-cutoff
        typezz=line.split('\t')[2]
        for valuez in range(int(d[number3].split('\t')[1])):
            genenum1 = e[number3][valuez]
            for valuezz in range(int(d[number4].split('\t')[1])):
                if typezz=='activation':
                    list8 = (genenum1.strip(),'::',e[number4][valuezz].strip(),'::True')
                    joinedlist8="".join(list8)
                    deap.write(joinedlist8+'\n')
                else:
                    list9 = (genenum1.strip(),'::',e[number4][valuezz].strip(),'::False')
                    joinedlist9="".join(list9)
                    deap.write(joinedlist9+'\n')
        
        
            
deap.close()  

b=[]
count = 1
for entry in root.findall('entry'):
    type1 = entry.get('type')
    if type1[1] == 'e':
        b.append(genelist[count-1].strip()+'\n')
    else:
        None
    count+=1

deap = str(open('deapformat_'+hsa_num,'r').readlines())
ab_genes = open('absentgenes_'+hsa_num,'w')
for gene_id in b:
    gene_id1=gene_id.strip()
    if re.search(gene_id1, deap):
        None
    else:
        ab_genes.write(gene_id1+'\n')
ab_genes.close()
