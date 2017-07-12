from extensions import connect_to_database
from misc import query_tables
import numpy as np
import matplotlib
# Save plot as png
matplotlib.use('Agg')
import matplotlib.pyplot as plt

db = connect_to_database()

prosp_per40_results, comps_per40_results = query_tables(db)

for prospect in prosp_per40_results:

    print(prospect['Player'])

    print(prospect['3PP'])
    print(prospect['FTP'])

    sim_shooting_percentages = {}

    if prospect['3PP'] is not 0.000 and prospect['3PA'] > 1.0:

        three_coords = []
        ft_coords = []
        sim_players = []

        for nba_player in comps_per40_results:

            title = prospect['Player'] + " similar 3P% (" + str(prospect['3PP']) + ") and FT% (" + str(prospect['FTP']) + ")"

            comp_key = nba_player['Player'] + ", " + nba_player['Season'] + ", " + nba_player['School']

            if nba_player['3PP'] is None or nba_player['3PA'] <= 1.0:
                nba_player['3PP'] = .000

            if prospect['3PP'] is None or prospect['3PA'] <= 1.0:
                prospect['3PP'] = .000

            three_diff = abs(float(nba_player['3PP']) - float(prospect['3PP']))
            FT_diff = abs(float(nba_player['FTP']) - float(prospect['FTP']))
            shot_diff = three_diff + FT_diff

            three_similar = three_diff <= .025
            FT_similar = FT_diff <= .025


            if three_similar and FT_similar:

                three_coords.append(three_diff)
                ft_coords.append(FT_diff)
                sim_players.append(nba_player['Player'].split(" ")[1])

                sim_shooting_percentages[comp_key] = (float(nba_player['3PP']), float(nba_player['FTP']), float("{0:.5f}".format(shot_diff)))

        sim_shooting_percentages = sorted(sim_shooting_percentages.items(), key=lambda x: x[1][2], reverse=False)

    print(sim_shooting_percentages)
    fig = plt.figure()
    fig.suptitle(title, fontsize=18)
    plt.xlabel('3P% Difference', fontsize=16)
    plt.ylabel('FT% Difference', fontsize=16)
    plt.xlim(-.001,.026)
    plt.ylim(-.001,.026)
    plt.scatter(three_coords, ft_coords)
    for i, txt in enumerate(sim_players):
        plt.annotate(txt, (three_coords[i],ft_coords[i]))

    plt.savefig('myfig')
    break



