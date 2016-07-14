import re

if __name__ == "__main__":

    g_code_contents = []

    with open("/home/jerry/Desktop/test.gcode") as f:
        for line in f:
            if line.startswith(';'):
                continue
            else:
                g_code_contents.append(line)

    extrutionless = [s for s in g_code_contents if "G0" in s]
    extrution = [s for s in g_code_contents if "G1" in s]

    total_g_codes = len(g_code_contents)
    total_extrutionless = len(extrutionless)
    total_extrution = len(extrution)
    ratio_align_to_printing = round((float)(total_extrutionless)/(total_extrution), 2)
    percentage_non_extrutionless = round((float)(total_extrutionless*100)/total_g_codes, 2)

    print "Total G-code entries:", total_g_codes
    print "Total extrution movements (printing):", total_extrution
    print "Total non-extrutionless movements (align):", total_extrutionless
    print "Ration align/printing (measure of inefficiency):", ratio_align_to_printing
    print "Percentage of align movements to total:", percentage_non_extrutionless, "%"


    print "\n"

    neighborhood_threshold = 2          #Change this value to change vicinity range
    print "Neighourhood threshold:", neighborhood_threshold

    #Process X values during extrution movement
    print "\n"
    print "X-axis statistics"
    X_in_extrution = [s for s in extrution if "X" in s]
    X_terms_in_extrution = []
    for line in X_in_extrution:
        X_term_list = re.search("(X)([\d]+[\.][\d]+)", line)
        X_terms_in_extrution.append(float(X_term_list.group(2)))

    X_groups = []
    transient_X_value = X_terms_in_extrution[1]


    group = []
    for value in X_terms_in_extrution:
        if (transient_X_value-neighborhood_threshold) <= value <= (transient_X_value+neighborhood_threshold):
            transient_X_value = value
            group.append(value)
        else:
            if not group:
                continue
            else:
                X_groups.append(group)
                transient_X_value = value
                group = []


    count_of_group_greater_than_size_ten = 0
    total_X_gcode_in_optimizable_lines = 0
    for group in X_groups:
        if len(group) > 10:
            count_of_group_greater_than_size_ten += 1
            total_X_gcode_in_optimizable_lines += len(group)

    percentage_optimizable_x = round((float)(total_X_gcode_in_optimizable_lines*100)/total_extrution, 2)

    print "Total number of linear X-movements groups:", count_of_group_greater_than_size_ten
    print "Total number of optimizable X-movements g-codes:", total_X_gcode_in_optimizable_lines
    print "Percentage of optimizable X-movements while printing:", percentage_optimizable_x, "%"




    #Process Y values during extrution movement
    print "\n"
    print "Y-axis statistics"
    Y_in_extrution = [s for s in extrution if "Y" in s]
    Y_terms_in_extrution = []
    for line in Y_in_extrution:
        Y_term_list = re.search("(Y)([\d]+[\.][\d]+)", line)
        Y_terms_in_extrution.append(float(Y_term_list.group(2)))

    Y_groups = []
    transient_Y_value = Y_terms_in_extrution[1]

    group = []
    for value in Y_terms_in_extrution:
        if (transient_Y_value-neighborhood_threshold) <= value <= (transient_Y_value+neighborhood_threshold):
            transient_Y_value = value
            group.append(value)
        else:
            if not group:
                continue
            else:
                Y_groups.append(group)
                transient_Y_value = value
                group = []


    count_of_group_greater_than_size_ten = 0
    total_Y_gcode_in_optimizable_lines = 0
    for group in Y_groups:
        if len(group) > 10:
            count_of_group_greater_than_size_ten += 1
            total_Y_gcode_in_optimizable_lines += len(group)

    percentage_optimizable_y = round((float)(total_Y_gcode_in_optimizable_lines*100)/total_extrution, 2)

    print "Total number of linear Y-movements groups:", count_of_group_greater_than_size_ten
    print "Total number of optimizable Y-movements g-codes:", total_Y_gcode_in_optimizable_lines
    print "Percentage of optimizable Y-movements while printing:", percentage_optimizable_y, "%"
