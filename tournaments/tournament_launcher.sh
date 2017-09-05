#!/bin/bash
mydate=`date +%s`; 

echo "STARTING TIME: " >> OUTPUT_tournament_$mydate;
echo `date` >> OUTPUT_tournament_$mydate;
echo "======================" >> OUTPUT_tournament_$mydate;
echo "" >> OUTPUT_tournament_$mydate;
python3 tournament.py >> OUTPUT_tournament_$mydate;
cat game_agent.py >> OUTPUT_tournament_game-agent_$mydate;
#python3 sample_players_mine.py >> OUTPUT_tournament_$mydate;
echo "" >> OUTPUT_tournament_$mydate;
echo "" >> OUTPUT_tournament_$mydate;
echo "ENDING TIME: " >> OUTPUT_tournament_$mydate;
echo `date` >> OUTPUT_tournament_$mydate; 
echo "======================" >> OUTPUT_tournament_$mydate;
echo "" >> OUTPUT_tournament_$mydate;
mydate_after=`date +%s`; 
total=$((mydate_after - $mydate)); 
echo "======================" >> OUTPUT_tournament_$mydate;
echo "======================" >> OUTPUT_tournament_$mydate;
echo "Total seconds: $total" >> OUTPUT_tournament_$mydate
echo "======================" >> OUTPUT_tournament_$mydate;
echo "======================" >> OUTPUT_tournament_$mydate;
