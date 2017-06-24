import sys

#init auc dict
params_auc_dict = {"last_ctr":1.1, "slot_show_sum":0, "slot_click_sum":0, \
                     "auc_temp":0.0, "click_sum":0.0, "old_click_sum":0.0, "no_click":0.0, \
                     "no_click_sum":0.0} 
#init q distribute
q_bucket = 1000
params_Q_dict = {"count_list":[0]*(q_bucket+1)}

for line in sys.stdin:
    lineL = line.strip().split('\t')

    if len(lineL) < 3:
        continue

    pctr = float(lineL[0])
    #print lineL[0]
    #pctr = float(lineL[0])/1e6
    show = int(float(lineL[1]))
    click = int(float(lineL[2]))
    slot_info = '-'
    
    ### calculate auc
    params_auc_dict["slot_show_sum"] += show
    params_auc_dict["slot_click_sum"] += click

    if params_auc_dict["last_ctr"] != pctr:
        params_auc_dict["auc_temp"] += (params_auc_dict["click_sum"] + \
                                         params_auc_dict["old_click_sum"]) * params_auc_dict["no_click"] / 2.0
        params_auc_dict["old_click_sum"] = params_auc_dict["click_sum"]
        params_auc_dict["no_click"] = 0.0
        params_auc_dict["last_ctr"] = pctr
    params_auc_dict["no_click"] += show - click
    params_auc_dict["no_click_sum"] += show - click
    params_auc_dict["click_sum"] += click
       
    ### calculate Q distribution
    index = int(pctr / (1.0/q_bucket)) #interval [0, 0.001) left close, right open
    count_list = params_Q_dict["count_list"]
    count_list[index] += show

# last instance for auc
params_auc_dict["auc_temp"] += (params_auc_dict["click_sum"] + \
         params_auc_dict["old_click_sum"]) * params_auc_dict["no_click"] / 2.0

if params_auc_dict["auc_temp"] > 0:
    auc = params_auc_dict["auc_temp"] / (params_auc_dict["click_sum"] * params_auc_dict["no_click_sum"])
else:
    auc = 0

print "AUC:%s\tshow_sum:%s\tclk_sum:%s" %( auc, params_auc_dict["slot_show_sum"], params_auc_dict["slot_click_sum"])

#print Q distribution result
for item in params_Q_dict:
    count_list = params_Q_dict["count_list"]
    print "Max bucket num: %s" %(sum(count_list))
    for i in range(q_bucket+1):
        if i < (q_bucket - 1):
            print str((i+1)*(1.0/q_bucket)) + '\t' + str(count_list[i])
        else:
            print '1.0\t' + str(count_list[i]+count_list[i+1])
            break
