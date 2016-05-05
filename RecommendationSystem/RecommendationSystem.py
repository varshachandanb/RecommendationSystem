import sys
import copy
import math
import itertools
from operator import itemgetter

def find_pairs():
    global user_ratings
    global neighbor_size
    global no_of_rec
    otpt=open("output.txt","w")
    pairs=[]
    pair_weights={}
    average_rating={}
    pred_rating={}
    unrated=[]
    rated=[]
    tmp=["$".join(map(str,comb)) for comb in itertools.combinations(items, 2)]
    for m in range(len(tmp)):
        itms=tmp[m].split('$')
        temp_items=[]
        temp_items.append(itms[0])
        temp_items.append(itms[1])
        pairs.append(temp_items)

    for m in pairs:
        temp1=""
        sum1=0.0
        sum2=0.0
        sum3=0.0
        div1=0.0
        item1=m[0]
        item2=m[1]
        avg1=0.0
        avg2=0.0
        common_count=0.0
        item1_list=[]
        item2_list=[]
        temp1=str(item1)+"$"+str(item2)
        data[item1] =sorted(data[item1],key=itemgetter(0))
        data[item2] =sorted(data[item2],key=itemgetter(0))

        for q in data[item1]:
            for r in data[item2]:
                if q[0] == r[0]:
                    item1_list.append(q)
                    item2_list.append(r)
        common_count=len(item1_list)
        for x in item1_list:
            avg1=avg1+float(x[1])
        for y in item2_list:
            avg2=avg2+float(y[1])
        if(common_count==0.0):
            average_rating[item1]=0.0
            average_rating[item2]=0.0
        else:
            average_rating[item1]=avg1/common_count
            average_rating[item2]=avg2/common_count
        for n in range(int(common_count)):
            sum1=sum1+(float(item1_list[n][1])-(average_rating[item1]))*(float(item2_list[n][1])-(average_rating[item2]))
            sum2=sum2+((float(item1_list[n][1])-(average_rating[item1]))**2)
            sum3=sum3+((float(item2_list[n][1])-(average_rating[item2]))**2)
        denom=(math.sqrt(sum2)*math.sqrt(sum3))
        if(denom==0.0):
            div1=0.0
        else:
            div1=sum1/denom
        pair_weights[temp1]=div1
        if("" in temp1):
            otpt.write(str(temp1)+str(pair_weights[temp1])+"\n")

    """for m in pair_weights:
        otpt.write("("+str(m)+') ,'+str(pair_weights[m])+'\n')"""

    for it in items:
        if it not in user_rated_items:
            unrated.append(it)

    unrated=list(set(unrated))
    user_ratings=sorted(user_ratings,key=itemgetter(0))

    for x in unrated:
        temp_ratings=copy.deepcopy(user_ratings)
        for y in range (len(temp_ratings)):
            pair1=str(temp_ratings[y][1])+'$'+str(x)
            pair2=str(x)+'$'+str(temp_ratings[y][1])
            for vl in pair_weights:
                if(pair1 == vl):
                    temp_ratings[y].append(pair_weights[pair1])
                elif pair2 == vl:
                    temp_ratings[y].append(pair_weights[pair2])

        temp_ratings=sorted(temp_ratings,key=itemgetter(1))
        temp_ratings=sorted(temp_ratings,key=itemgetter(2),reverse=True)
        add1=0.0
        add2=0.0
        dv=0.0
        c=0
        if (len(temp_ratings)<neighbor_size):
            neighbor_size=len(temp_ratings)
        for z in range(neighbor_size):
            p1=str(temp_ratings[z][1])+'$'+str(x)
            p2=str(x)+'$'+str(temp_ratings[z][1])
            for val in pair_weights:
                if(p1 == val):
                    add1+=(float(temp_ratings[z][0])*pair_weights[p1])
                    add2+=float(abs(pair_weights[p1]))
                elif(p2 ==val):
                    add1+=(float(temp_ratings[z][0])*pair_weights[p2])
                    add2+=float(abs(pair_weights[p2]))

        if(add2==0.0):
            pred_rating[x]=0.0
        else:
            dv=float(add1/add2)
            dv=round(dv,5)
            pred_rating[x]=dv
    pred_rating = sorted(pred_rating.items(), key=itemgetter(0))
    pred_rating = sorted(pred_rating, key=itemgetter(1),reverse=True)
    if(len(pred_rating)<no_of_rec):
        no_of_rec=len(pred_rating)
    """for a in range(no_of_rec):
        otpt.write(str(pred_rating[a][0])+' '+str(pred_rating[a][1])+'\n')"""
    for a in range(no_of_rec):
        print(str(pred_rating[a][0])+' '+str(pred_rating[a][1]))


    otpt.close()

if __name__ == '__main__':
    ratingsFileName=sys.argv[1]
    inpt=open(ratingsFileName,"r")
    user=str(sys.argv[2])
    neighbor_size=int(sys.argv[3])
    no_of_rec=int(sys.argv[4])
    data={}
    items=[]
    user_ratings=[]
    user_rated_items=[]
    lines=inpt.readlines()
    for i in range(len(lines)):
        lines[i]=lines[i].strip()
        temp1=[]
        temp2=[]
        line=lines[i].split('\t')
        if (line[2] not in data):
            data[line[2]]=[]
        temp1.append(str(line[0]))
        temp1.append(str(line[1]))
        data[line[2]].append(temp1)
        items.append(line[2])
        if(line[0] == user):
            temp2.append(str(line[1]))
            temp2.append(str(line[2]))
            user_ratings.append(temp2)
            user_rated_items.append(str(line[2]))
    items=list(set(items))
    items=sorted(items)
    inpt.close()
    find_pairs()



