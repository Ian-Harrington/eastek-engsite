# takes a tuple of tuples ((db,human),...) and db entry returns the human-readable version 
# better option is to {% load custom %} in the template 
#   and the use the |human_readable:<list> filter  
def choice_lookup(opt_list, item):
	for i in range(len(opt_list)):
		if opt_list[i][0] == item:
			return opt_list[i][1]
	else:
		return None