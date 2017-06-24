
# -*- coding: gbk -*-

import sys

show_dic = dict()
clk_dic = dict()
if __name__ == '__main__':
    for line in sys.stdin:
        data = line.strip('\n').split('\t')
        pctr = int(data[0])
        if pctr in show_dic:
            show_dic[pctr] = show_dic.get(pctr,0) + float(data[1])
            clk_dic[pctr] = clk_dic.get(pctr, 0) + float(data[2])
        else:
            show_dic[pctr] = int(data[1])
            clk_dic[pctr] = int(data[2])

    for i,j in sorted(show_dic.iteritems(), key=lambda d: d[0] , reverse=True):
        print float(i)/1e6,"\t",show_dic[i],'\t',clk_dic[i]

