import pandas as pd

def main():
    dir = '../text_data/name_count.csv'
    df = pd.read_csv(dir,header=None)
    group_name_entities(df)

##TODO: Group every name entity manually.
def group_name_entities(series):
    match_first_name = input("Match first name:")
    match_middle_name = input("Match middle name:")
    match_last_name = input("Match last name:")

    names = series[0].values
    counts = series[1].values
    sum = 0

##TODO: Simply find the combination of different name entities expression in the novel
    if match_middle_name=='None':
        f = open('../Characters_directory/{}_{}.txt'.format(match_first_name, match_last_name), 'w+')
        for i in range(len(names)):
            if match_first_name.title() in names[i] or match_first_name.lower() in names[i] or match_first_name in names[i] \
                    or match_last_name.title() in names[i] or match_last_name.lower() in names[i] or match_last_name in names[i] \
                    or 'Professors {}'.format(match_last_name) == names[i] \
                    or 'Miss {}'.format(match_last_name)==names[i] \
                    or 'Mr {}'.format(match_last_name)==names[i] \
                    or 'Mrs {}'.format(match_last_name)==names[i] \
                    or 'Uncle {}'.format(match_last_name) == names[i]\
                    or 'Aunt {}'.format(match_last_name) == names[i]:

                if counts[i] > 1:
                    f.writelines('{}'.format(names[i]))
                    f.write('\n')
                sum = sum + counts[i]

    else:
        f = open('../Characters_directory/{}_{}_{}.txt'.format(match_first_name, match_middle_name, match_last_name), 'w+')
        for i in range(len(names)):
            if match_first_name.title() in names[i] or match_first_name.lower() in names[i] or match_first_name in names[i] \
                    or match_last_name.title() in names[i] or match_last_name.lower() in names[i] or match_last_name in names[i] \
                    or match_middle_name.title() in names[i] or match_middle_name in names[i] or match_middle_name.lower() in names[i] \
                    or 'Professors {}'.format(match_last_name) == names[i] \
                    or 'Miss {}'.format(match_last_name)==names[i] \
                    or 'Mr {}'.format(match_last_name)==names[i] \
                    or 'Mrs {}'.format(match_last_name)==names[i] \
                    or 'Uncle {}'.format(match_last_name) == names[i] \
                    or 'Aunt {}'.format(match_last_name) == names[i]:

                if counts[i] > 1:
                    f.writelines('{}'.format(names[i]))
                    f.write('\n')
                sum = sum + counts[i]

    print('Total amount of {} is {}.'.format(match_first_name,sum))
    f.close()


##TODO: After first combination, still need manual selection in .txt file.

if __name__ == '__main__':
    main()

