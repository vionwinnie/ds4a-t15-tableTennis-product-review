import fuzzywuzzy
import re 
import pandas as pd

pattern = """[a-zA-Z0-9 -]+"""
p = re.compile(pattern)

title = ['Tenergy 05FX vs Tenergy 64FX',
 'Butterfly Impartial XS vs 802-40 vs spinlord waran2',
 'What is the difference between Apalonia ZLC vs Innerforce ZLC',
 'Tenergy 05 vs Tenergy 80',
 'New Viscaria vs Old Viscaria',
 'Tenergy 64 vs 80 On BH',
 'Tenenergy 05 vs Donic Baracuda',
 'Tenenergy 05 vs Donic Baracuda',
 'Tenenergy 05 vs Donic Baracuda',
 'Tenergy (1.9 vs 2.1 weight) on Timo Boll ALC and Jun Mizutani',
 'Tenergy 64 vs Tenergy 64 fx vs Tenergy 05 vs Tenergy 05 fx',
 'Tibhar Evo EL-P vs FX-P for flicks and brushing loops',
 'EL-P vs EL-S, Any Experiences, Please share',
 'FX-P vs FX-S',
 'Mizuno GF T40 vs Nittaku Fastarc S-1',
 'Stiga genesis m vs mantra m on bh',
 'Gold arc 8 vs tenergy 05',
 'Need a new BH rubber: O7P vs DNA Pro M?',
 'Skyline TG2 NEO vs Hurricane 3 NEO',
 'DHS Hurricane 3 National (Blue Sponge) vs the NEO version of it',
 'Donic BlueStrom Z2 vs Xiom Omega V Asia for fh? (on a Stiga Offensive Nct CS)',
 'TIBHAR EL-P vs MX-P',
 'aurus vs rakza 7',
 'DHS Goldarc 8 vs Stiga Mantra M',
 'Revspin Rubber Ratings',
 'Omega VII Asia vs Hurricane 3',
 'Palio Hadou 40+ vs Ak47 Yellow',
 'Fastarc G-1 (vs. Baracuda)',
 'Rakza 7 vs Evolution MX-S?',
 'Tibhar Genius (vs Donic Baracuda)',
 'Nittaku FastArc G1 vs DHS Hurricane 3 Neo Commercial',
 'DHS vs. Tensor - long term investment',
 'Which one do you prefer on BH between EL-P vs EL-S',
 'DHS Hurricane 3-50 soft vs Hurricane 8',
 'Tenergy 05 max vs 05 1.9',
 'Xiom Vega Pro vs Tibhar Evolution MX-P',
 'Xiom vega pro vs neo 3?',
 'Tensor vs chinese',
 'Andro Rasanter R47 and R50 vs Butterfly Tenergy 05',
 'Rakza 7 soft MAX VS Tibhar Evo EL-S 1.9 on BH ?',
 'MX-S vs. Genesis M',
 'Joola rhyzm vs rhyzm tech',
 'tibhar quantum S vs evo EL-P',
 'Please compare durability Rakza X vs Evo MX-S',
 'Rubber for FH , Acuda Blue P1 vs Evo MX-S vs Rakza x',
 'What do you prefer? Chinese Rubber vs European Rubbers?',
 'Hurricane 3 neo vs Hurricane 8',
 'Stiga Mantra vs Genesis',
 'Mx-p VS Xiom Sigma 2 Europe Europe',
 'Xiom Sigma II Europe vs tenergy 05, mx-p',
 'Yasaka Rising Dragon vs Chinese tacky rubbers',
 'Ttnpp vs prott',
 'globe 999 national vs dhs hurricanes and skylines',
 'Donic Bluefire M1 turbo vs Nittaku Fastarc G-1',
 'H3 Neo Provincial vs Commercial',
 'Tenergy 05 vs Tibhar Evolution MX-S vs Donic Acuda Blue P1',
 'Acuda S2 vs Vega japan',
 'Rakza 7 vs Calibra Lt pros cons which one is the one?',
 'Butterfly Spinart vs Yinhe Big Dipper vs Haifu Blue Whale 2',
 'Chinese Rubber vs European Rubbers. What are the key differences?',
 'Timo Boll ALC + Mark Vs or Srivers?',
 'Baracuda vs coppa x1 gold vs rakza 7',
 'Chinese vs Euro rubbers',
 'backhand advice T05fx vs. T64',
 'Bluefire jp 01 vs Bluefire M1',
 'H3Neo vs SkylineIII',
 'DHS Memo 2 vs Yasaka Mark V',
 'Hurricane 3 blue sponge vs skyline 3 blue sponge',
 'Soft vs Hard Rubbers',
 'Hard vs soft rubbers',
 'Calibra LT Spin vs Calibra LT Sound',
 'DHS Skyline 3 Neo vs. Hurricane 3 Neo']


for cur_title in title:
    cur_title = cur_title.replace('VS','vs')
    cur_title = cur_title.replace('Vs','vs')
    tmp_split = cur_title.split('vs')
    tmp_split_stripped = [tmp.strip() for tmp in tmp_split]
    
    for rubber in tmp_split_stripped:
        print(re.search(p,rubber)[0])


