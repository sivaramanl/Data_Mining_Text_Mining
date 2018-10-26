# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 03:05:19 2018

@author: Sivaraman Lakshmipathy, Lakshmi Divya Jillellamudi Kamala
"""

#ms-ps

import math
    
class ms_ps:
    data_file_name = ""
    params_file_name = ""
    result_file_name = ""
    S = []
    mis_ip = {} #contains the given mis values as list [count_val, percentage_val]
    SDC = 1
    size_1_items = []
    cx_count = 0
    output_freq_count = {}
    #store frequent itemsets with corresponding support
    frequent_itemsets = {}
    level_1_freq_items_sorted = []
    level_1_itemsets = []
    level_1_itemsets_count = {}
    
    def find_freq_items(self, alpha, S_a):
        return
    
    def construct_size_1_frequent_itemset(self, item):
        return "{" + item + "}"
    
    def construct_freq_itemset(self, alpha, item):
        if "{" not in alpha:
            if "_" not in item:
                return self.construct_size_1_frequent_itemset(item)
            else:
                print("Unexpected pattern encountered:", item, " Not processing.")
                return
        if "_" in item:
            last_index = alpha.rfind("{")
            last_seq = alpha[last_index:len(alpha)-1]
            temp_end = last_seq + "," + item[1:] + "}"
            return alpha[:last_index] + temp_end
        else:
            return alpha + self.construct_size_1_frequent_itemset(item)
        return
    
    def is_item_present(self, entry, item):
        entry = entry[1:len(entry)-1]
        sequences = entry.split("}")
        for i in range(0, len(sequences)):
            if len(sequences[i]) == 0:
                del sequences[i]
            else:
                if "{" in sequences[i]:
                    sequences[i] = sequences[i][1:]
                #enumerate the distinct items and update their corresponding counts
                distinct_items = sequences[i].split(",")
                for d_item in distinct_items:
                    if d_item == item:
                        return True
        return False
    
    def custominarray(self,x,y,index):
        flag = False
        prev_indx = -1
        for item in y:
            if item in x:
                indx = x.index(item)
                if indx<index and indx > prev_indx:
                    prev_indx = indx
                    flag = True
                else:
                    flag = False
                    break
            else:
                flag = False
                break
        return flag
    
    def construct_projection(self, S, freq_item, prefix, freq_itemsets, ik, last_prefix, alpha):
        underscore_mode = False
        if "_" in freq_item:
            underscore_mode = True
        modified_freq_item = ""
        if len(last_prefix) > 0:
            modified_freq_item = last_prefix
        final_projection = []
        for entry in S:
            appendToProjection = False
            ik_presence = False
            if self.is_item_present(alpha, ik):
                ik_presence = True
            projected_sequence = ""
            entry = entry[1:len(entry)-1]
            sequences = entry.split("}")
            for i in range(0, len(sequences)):
                encountered_underscore = False
                if len(sequences[i]) == 0:
                    del sequences[i]
                else:
                    if appendToProjection:
                        projected_sequence += "{"
                    if "{" in sequences[i]:
                        sequences[i] = sequences[i][1:]
                    #enumerate the distinct items and update their corresponding counts
                    distinct_items = sequences[i].split(",")
                    for d_item in distinct_items:
                        if "_" == d_item:
                            if underscore_mode == False:
                                break
                            else:
                                encountered_underscore = True
                                continue
                        if d_item == ik and appendToProjection == True:
                            ik_presence = True
                        if appendToProjection == True:
                            if projected_sequence[-1:] != '{':
                                projected_sequence += ","
                            projected_sequence += d_item
                        else:
                            if d_item == freq_item or (d_item == str(freq_item[1:]) and encountered_underscore == True):
                                if "," in sequences[i]:
                                    appendToProjection = True
                                    projected_sequence = "{_"
                                else:
                                    appendToProjection = True
                            elif d_item == str(freq_item[1:]) and underscore_mode == True:
                                indx = distinct_items.index(d_item)
                                temp_item_list = modified_freq_item.split(",")
                                try:
                                    temp_appendToProjection = self.custominarray(distinct_items, temp_item_list, indx)
                                except IndexError:
                                    temp_appendToProjection = False
                                    break
                                if temp_appendToProjection == True:
                                    if "," in sequences[i]:
                                        appendToProjection = True
                                        projected_sequence = "{_"
                                    else:
                                        appendToProjection = True
                    if appendToProjection == True and len(projected_sequence)>0:
                        projected_sequence += "}"
                    if "{_}" in projected_sequence:
                        projected_sequence = projected_sequence.replace("{_}", "")
                    if "{}" in projected_sequence:
                        projected_sequence = projected_sequence.replace("{}", "")
            if len(projected_sequence) > 0 and ik_presence == True:
                final_projection.append(projected_sequence)
        return final_projection
    
    def PrefixSpan(self, alpha, l, S_a):
        if not S_a:
            #projected database is empty.
            return
        freq_items = self.find_freq_items(alpha, S_a)
        if not freq_items:
            return
        for item in freq_items:
            alpha_prime = self.construct_freq_itemset(alpha, item)
            self.frequent_itemsets[alpha_prime] = freq_items.get(item)
            S_a_prime = self.construct_projection(S_a, alpha, alpha_prime)
            self.PrefixSpan(alpha_prime, l+1, S_a_prime)
        return
    
    def identify_frequent_items(self, items, items_count, minsup):
        freq_it = []
        for it in items:
            if items_count[it] >= minsup:
                freq_it.append(it)
        return freq_it
    
    def r_prefixScan(self, ik, Sk, ik_mis, alpha, alpha_count, size_1_items):
        if not Sk: #the dataset is empty
            return
        last_prefix = alpha[alpha.rfind("{")+1:len(alpha)-1]
        itemsets, itemsets_count = self.generate_itemsets(Sk, size_1_items, last_prefix)
        freq_itemsets = self.identify_frequent_items(itemsets, itemsets_count, ik_mis)
        if not freq_itemsets:
            return
        for item in freq_itemsets:
            alpha_prime = self.construct_freq_itemset(alpha, item)
            alpha_prime_count = itemsets_count[item]
            Sk_proj = self.construct_projection(Sk, item, alpha, freq_itemsets, ik, last_prefix, alpha_prime)
            next_level_item = item
            if "_" in next_level_item:
                next_level_item = next_level_item[1:]
            if self.is_item_present(alpha_prime, ik):
                if alpha == "" or (alpha != "" and self.satisfy_sdc_check(alpha_prime)):
                    self.add_to_output(alpha_prime, itemsets_count[item])
            self.r_prefixScan(ik, Sk_proj, self.mis_ip[str(ik)][0], alpha_prime, itemsets_count[item], size_1_items)
            
    def add_to_output(self, seq, seq_count):
        number_of_items_in_seq = 0
        sequences = seq.split("}")
        for i in range(0, len(sequences)):
            if len(sequences[i]) == 0:
                del sequences[i]
            else:
                if "{" in sequences[i]:
                    sequences[i] = sequences[i][1:]
                distinct_items = sequences[i].split(",")
                for d_item in distinct_items:
                    number_of_items_in_seq += 1
        new_entry = {seq : seq_count}
        if number_of_items_in_seq in self.output_freq_count:
            old_seq = self.output_freq_count[number_of_items_in_seq]
            if seq not in old_seq:
                old_seq[seq] = seq_count
                self.output_freq_count[number_of_items_in_seq] = old_seq
        else:
            self.output_freq_count[number_of_items_in_seq] = new_entry
            
    def get_mis(self, sequence1, sequence2):
        mis1 = self.get_misforsequence(sequence1)
        mis2 = self.get_misforsequence(sequence2)
        if mis1 == -1:
            return mis2
        elif mis2 == -1:
            return mis1
        elif mis1 < mis2:
            return mis1
        return mis2
    
    def get_misforsequence(self,seq):
        min_mis = -1
        sequences = seq.split("}")
        for i in range(0, len(sequences)):
            if len(sequences[i]) == 0:
                del sequences[i]
            else:
                if "{" in sequences[i]:
                    sequences[i] = sequences[i][1:]
                #enumerate the distinct items and update their corresponding counts
                distinct_items = sequences[i].split(",")
                for d_item in distinct_items:
                    if "_" in d_item:
                        d_item = d_item[1:]
                    local_mis = self.mis_ip[str(d_item)][0]
                    if min_mis == -1 or local_mis < min_mis:
                        min_mis = local_mis
        return min_mis
        
    def populate_output_file(self, output):
        file_obj = open(self.result_file_name, "w")
        endline = "\n"
        
        i = 1
        output_keys = output.keys()
        while True:
            if i not in output_keys:
                break
            size_i_pattern = output[i]
            str1 = "The number of length " + str(i) + " sequential patterns is " + str(len(size_i_pattern))
            file_obj.write(str1)
            file_obj.write(endline)
            for item in size_i_pattern:
                str2 = "Pattern : <" + item.replace(",", " ") + ">:Count=" + str(size_i_pattern[item])
                file_obj.write(str2)
                file_obj.write(endline)
            i += 1
        file_obj.close()
        
    def populate_S(self):
        cx_counter = 0
        file_obj = open(self.data_file_name, "r")
        for line in file_obj:
            self.S.append(line.strip().replace(" ", "").replace("\t", ""))
            cx_counter += 1
        self.cx_count = cx_counter
        return;
    
    def populate_params(self):
        file_obj = open(self.params_file_name, "r")
        for line in file_obj:
            if "SDC" in line:
                self.SDC = float((line.split("=")[1]).strip())
            elif "MIS" in line:
                temp_var = line.split("=")
                #extract item from 1st token
                item = (temp_var[0][temp_var[0].index('(')+1:temp_var[0].index(')')]).strip()
                mis_val = float(temp_var[1].strip())
                self.mis_ip[str(item)] = [math.ceil(mis_val*self.cx_count), mis_val]
        
    def __init__(self, ip_file_list):
        file_obj = open(ip_file_list, "r")
        self.data_file_name = "ms_ps_data.txt"
        self.params_file_name = "ms_ps_params.txt"
        self.result_file_name = "ms_ps_result.txt"
        for line in file_obj:
            if "Data file:" in line:
                self.data_file_name = line.split(":")[1].strip()
            elif "Params file:" in line:
                self.params_file_name = line.split(":")[1].strip()
            elif "Result file:" in line:
                self.result_file_name = line.split(":")[1].strip()
        
    def update_enumerated_items(self, items_list, items_counter, local_items_list):
        for it in local_items_list:
            if it in items_counter:
                items_counter[str(it)] += 1
            else:
                #insert in correct index
                indx = 0
                if not items_list:
                    items_list.append(it)
                else:
                    is_inserted = False
                    for global_it in items_list:#Basically sorting and storing 
                        temp_it = it
                        temp_global_it = global_it
                        if '_' in it:
                            temp_it = it[1:]
                        if '_' in global_it:
                            temp_global_it = global_it[1:]
                        
                        if temp_it.isdigit() and temp_global_it.isdigit():
                            if int(temp_global_it) > int(temp_it):
                                items_list.insert(indx, it)
                                is_inserted = True
                                break
                        else:
                            if temp_global_it > temp_it:
                                items_list.insert(indx, it)
                                is_inserted = True
                                break
                        indx += 1
                    if is_inserted == False:
                        items_list.append(it)
                    
                items_counter[str(it)] = 1
        return items_list, items_counter
    
    def identify_level_1_frequent_items(self, items, items_count):
        freq_it = []
        for it in items:
            if '_' in it:
                it = it[1:]
            if items_count[str(it)] >= self.mis_ip[str(it)][0]:
                freq_it.append(it)                                                                                                                                                 
        return freq_it
    
    def generate_level_1_itemsets(self, S):
        return self.generate_itemsets(S, [], "")
        
    def generate_itemsets(self, S, prev_enumerated_items, last_prefix):
        #iterate through S, enumerate all distinct items
        enumerated_items = []
        enumerated_items_count = {}
        #Step 1: split into transactions
        for entry in S:
            local_enumerated_items = []
            entry = entry[1:len(entry)-1]
            sequences = entry.split("}")
            for i in range(0, len(sequences)):
                local_prefix = ''
                if len(sequences[i]) == 0:
                    del sequences[i]
                else:
                    if "{" in sequences[i]:
                        sequences[i] = sequences[i][1:]
                    #enumerate the distinct items and update their corresponding counts
                    #print(sequences[i])
                    distinct_items = sequences[i].split(",")
                    for d_item in distinct_items:
                        if d_item == '_':
                            local_prefix = '_'
                            continue
                        if d_item in local_enumerated_items and local_prefix == '':
                            continue
                        elif d_item in local_enumerated_items and local_prefix != '':
                            if "_" + d_item in local_enumerated_items:
                                continue
                        else:
                            if local_prefix == '_':
                                local_enumerated_items.append(local_prefix+d_item)
                            else:
                                local_enumerated_items.append(d_item)
            enumerated_items, enumerated_items_count = self.update_enumerated_items(enumerated_items, enumerated_items_count, local_enumerated_items)
            
        for l_item in enumerated_items:
                if "_" in l_item:
                    modified_l_item = last_prefix
                    for entry in S:
                        projection_completed_for_entry = False
                        entry = entry[1:len(entry)-1]
                        sequences = entry.split("}")
                        underscore_value_presence = False
                        for i in range(0, len(sequences)):
                            if len(sequences[i]) == 0:
                                del sequences[i]
                            elif projection_completed_for_entry == True:
                                break
                            else:
                                if "{" in sequences[i]:
                                    sequences[i] = sequences[i][1:]
                                #enumerate the distinct items and update their corresponding counts
                                distinct_items = sequences[i].split(",")
                                underscore_presence = False
                                for d_item in distinct_items:
                                    if d_item == "_":
                                        underscore_presence = True
                                        continue
                                    elif d_item == l_item[1:]:
                                        if underscore_presence == True:
                                            underscore_value_presence = True
                                            continue
                                        if underscore_value_presence == True:
                                            continue
                                        temp_item_list = modified_l_item.split(",")
                                        temp_appendToProjection = True
                                        indx = distinct_items.index(d_item)
                                        try:
                                            temp_appendToProjection = self.custominarray(distinct_items, temp_item_list, indx)
                                        except IndexError:
                                            temp_appendToProjection = False
                                            break
                                        if temp_appendToProjection == True:
                                            projection_completed_for_entry = True
                                            if l_item in enumerated_items_count:
                                                enumerated_items_count[l_item] += 1
                                            else:
                                                enumerated_items.append(l_item)
                                                enumerated_items_count[l_item] = 1
                                                break
                                            
        return enumerated_items, enumerated_items_count
    
    def sort_by_mis(self, list):
        sorted_list = []
        for item in list:
            indx = 0
            for it in sorted_list:
                if self.mis_ip[str(it)] <= self.mis_ip[str(item)]:
                    indx += 1
                else: break
            sorted_list.insert(indx, item)
        return sorted_list
    
    def satisfy_sdc(self, item1_count, item2_count):
        return abs((item1_count - item2_count)/self.cx_count) <= self.SDC
    
    def satisfy_sdc_check(self, seq):
        sequences = seq.split("}")
        unique_items = []
        for i in range(0, len(sequences)):
            if len(sequences[i]) == 0:
                continue
            else:
                if "{" in sequences[i]:
                    sequences[i] = sequences[i][1:]
                #enumerate the distinct items and update their corresponding counts
                distinct_items = sequences[i].split(",")
                for d_item in distinct_items:
                    if d_item not in unique_items:
                        unique_items.append(d_item)
        for i in range(0, len(unique_items)):
            for j in range(i+1, len(unique_items)):
                if self.satisfy_sdc(self.level_1_itemsets_count[unique_items[i]], self.level_1_itemsets_count[unique_items[j]]) == False:
                    return False
        return True
    
    def construct_modified_entry(self, entry, processed_list, ik, items_count):
        entry = entry[0:]
        modified_entry = ""
        entry = entry[1:len(entry)-1]
        sequences = entry.split("}")
        for i in range(0, len(sequences)):
            local_sequence = ""
            if len(sequences[i]) == 0:
                continue
            else:
                if "{" in sequences[i]:
                    sequences[i] = sequences[i][1:]
                #enumerate the distinct items and update their corresponding counts
                distinct_items = sequences[i].split(",")
                for d_item in distinct_items:
                    if d_item in processed_list:
                        continue
                    if self.satisfy_sdc(items_count[str(ik)], items_count[str(d_item)]) == False:
                        continue
                    else:
                        if local_sequence == "":
                            local_sequence += d_item
                        else:
                            local_sequence += "," + d_item
            if local_sequence != "":
                modified_entry += "{" + local_sequence + "}"
        #return entry
        return modified_entry
    
    def identify_sequences(self, S, ik, processed_list, items_count):
        S1 = []
        for entry in S:
            check_flag = False
            entry = entry[1:len(entry)-1]
            sequences = entry.split("}")
            for i in range(0, len(sequences)):
                if len(sequences[i]) == 0:
                    continue
                else:
                    sequences[i] = sequences[i][1:]
                    #enumerate the distinct items and update their corresponding counts
                    distinct_items = sequences[i].split(",")
                    for d_item in distinct_items:
                        if d_item == ik:
                            S1.append(self.construct_modified_entry(entry, processed_list, ik, items_count))
                            check_flag = True
                            break
                if check_flag == True: break
        
        return S1
        
    def generate_frequent_itemsets_ms_ps(self):
        self.populate_S()
        self.level_1_itemsets, self.level_1_itemsets_count = self.generate_level_1_itemsets(self.S)
        self.populate_params()
        
        #Step 1 in algo: Find items with support >= MIS
        level_1_freq_items = self.identify_level_1_frequent_items(self.level_1_itemsets, self.level_1_itemsets_count)
        #Step 2 in algo: Sort by MIS
        self.level_1_freq_items_sorted = self.sort_by_mis(level_1_freq_items)
        processed_freq_items = []
        
        #Step 3 in algo:
       
        for ik in self.level_1_freq_items_sorted:
            #Step 3.1
            Sk = self.identify_sequences(self.S, ik, processed_freq_items, self.level_1_itemsets_count)
            #Step 3.2
            self.r_prefixScan(ik, Sk, self.mis_ip[str(ik)][0], "", 0, self.level_1_itemsets)
            processed_freq_items.append(ik)
        
        self.populate_output_file(self.output_freq_count)
        return
        
def main():
    input_file = "ms_ps_file_list.txt"
    try:
        ms_ps_processor = ms_ps(input_file)
    except:
        print("Error while reading the input. Please verify the location of the file containing the list of input files")
        return
    ms_ps_processor.generate_frequent_itemsets_ms_ps()

if __name__ == '__main__':
    main()  
