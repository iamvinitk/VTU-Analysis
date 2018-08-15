import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

result_file = input("Enter the file name of the result file (eg. result.csv)")
df = pd.read_csv(result_file)
col_list = ['USN', 'SCx', 'SNx', 'Internalx', 'Externalx', 'Totalx', 'Resultx', 'Gradex', 'GradeTotalx']


def get_results(data_frame):
    passed_stud_df = data_frame.loc[data_frame[col_list[6]] == 'P']

    total_stud = data_frame.shape[0]
    passed_stud = passed_stud_df.shape[0]
    failed_stud = total_stud - passed_stud
    plot_sub_graph(passed_stud, failed_stud, data_frame.iloc[0][1], data_frame.iloc[0][2])
    bar_graph = data_frame[col_list[5]].tolist()
    print(bar_graph)

    fig = plt.figure(2, figsize=(8, 4.5))
    fig.tight_layout()
    bins = [0, 39, 44, 49, 59, 69, 79, 89, 100]
    plt.hist(bar_graph, bins, histtype="bar", rwidth=0.6)
    plt.title(data_frame.iloc[0][1] + "\n" + data_frame.iloc[0][2])
    plt.xlabel("Marks")
    plt.ylabel("No. of Students")
    plt.xticks(bins)

    plt.savefig(data_frame.iloc[0][1] + '-bar.png', format='png', dpi=250)
    plt.show()


def plot_sub_graph(passed_stud, failed_stud, sub_code, sub_name):
    fig, ax = plt.subplots(figsize=(8, 4.5), subplot_kw=dict(aspect="equal"))
    data = [passed_stud, failed_stud]
    labels = [str(passed_stud) + " Passed", str(failed_stud) + " Failed"]
    explode = (0, 0.2)
    wedges, texts, autotexts = ax.pie(data, autopct='%1.1f%%', explode=explode,
                                      textprops={'color': "w"})
    ax.legend(wedges, labels,
              title="No of Students",
              loc="best",
              bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=10, weight="bold")

    ax.set_title(sub_code + "\n" + sub_name)
    plt.savefig(sub_code + '.png', format='png', dpi=250)


subject_code_list = []


def subject_wise(required_stud):
    for i in range(1, 9):
        subject_code_list.append('SC' + str(i))
    scs = np.unique(required_stud[subject_code_list].values)
    for i, val in enumerate(scs):
        print("Enter " + str(i) + " for " + val)
    print("Enter 99 for all Subjects")
    # Input the Subject code
    option = int(input())
    if option == 99:
        for j in scs:
            select_sub(required_stud, j)
    else:
        select_sub(required_stud, scs[option])


def select_sub(required_stud, subject_code):
    subject_col = ''
    print(subject_code)
    student_of_subject_code = []
    for i in range(1, 9):
        if required_stud.index[required_stud['SC' + str(i)] == subject_code].tolist():
            subject_col = i
            student_of_subject_code = required_stud.index[required_stud['SC' + str(i)] == subject_code].tolist()
            break

    for i in range(1, 9):
        col_list[i] = col_list[i][:-1] + str(subject_col)
    get_results(required_stud.loc[student_of_subject_code, col_list])


def xyz(required_stud):
    sub_option = int(input("Enter 1 for Subject Wise or 2 Combined Result"))
    total_stud = required_stud.shape[0]
    if sub_option == 1:
        subject_wise(required_stud)
    elif sub_option == 2:
        total_passed = 0
        pass_stud = [0] * 8
        for usn in list(required_stud.iloc[:, 0]):
            count = 0
            part_stud = required_stud.loc[required_stud['USN'] == usn]
            for i in range(0, 8):
                if part_stud.loc[part_stud['Result' + str(1 + i)].isin(["P"])].shape[0] == 1:
                    count += 1
                    pass_stud[i] += 1

            if count == 8:
                total_passed += 1
                print(usn, ": Passed in all")
            else:
                print(usn, ": Failed in ", 8 - count)

        for i, value in enumerate(pass_stud):
            pass_stud[i] = round((pass_stud[i] / total_stud) * 100, 2)
        print(pass_stud)

        plot_sub_graph(total_passed, total_stud - total_passed, "Overall", "Result")


def usnwise_or_all():
    option = int(input("Enter 1 for specific USN's or 2 for all"))
    if option == 1:
        usn_file = input("Enter the file name of USN as specified in sample (eg. usn.csv)")
        usn_list = pd.read_csv(usn_file, header=None)  # Pass USN filename
        usn_list = (list(usn_list.iloc[0]))
        required_stud = df.loc[df['USN'].isin(usn_list)]
        xyz(required_stud)
    elif option == 2:
        xyz(df)


usnwise_or_all()

# usn_list = (list(usn_list.iloc[0]))
# # print(df)
# # print(df.keys())
# total_passed = 0
# required_stud = df.loc[df['USN'].isin(usn_list)]
# total_stud = required_stud.shape[0]
# pass_stud = [0] * 8
# for usn in list(required_stud.iloc[:, 0]):
#     count = 0
#     part_stud = required_stud.loc[required_stud['USN'] == usn]
#     # print(part_stud)
#     for i in range(0, 8):
#         if part_stud.loc[part_stud['Result' + str(1 + i)].isin(["P"])].shape[0] == 1:
#             count += 1
#             pass_stud[i] += 1
#
#     if count == 8:
#         total_passed += 1
#         print(usn, ": Passed in all")
#     else:
#         print(usn, ": Failed in ", 8 - count)
#
# for i, value in enumerate(pass_stud):
#     pass_stud[i] = round((pass_stud[i] / total_stud) * 100, 2)
# print(pass_stud)
#
# labels = 'Total Pass', 'Total Fail'  # , 'SC2', 'SC3', 'SC4', 'SC5', 'SC6', 'SC7', 'SC8'
# sizes = total_passed, total_stud - total_passed
# explode = (0, 0.2)
#
# fig1, ax1 = plt.subplots()
# ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#         shadow=False, startangle=45)
# ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
# plt.title('Total Result')
# fig1.savefig('Total Result.png')  # save the figure to file
# plt.show()
#
# for i in range(len(pass_stud)):
#     labels = 'SC' + str(i + 1) + 'Pass', 'SC' + str(i + 1) + 'Fail'  # , 'SC2', 'SC3', 'SC4', 'SC5', 'SC6', 'SC7', 'SC8'
#     sizes = pass_stud[i], 100 - pass_stud[i]
#     explode = (0, 0.2)
#
#     fig1, ax1 = plt.subplots()
#     ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
#             shadow=False, startangle=45)
#     ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     plt.title('SC' + str(i + 1))
#     fig1.savefig('SC' + str(i + 1) + '.png')  # save the figure to file
#     plt.show()
#
