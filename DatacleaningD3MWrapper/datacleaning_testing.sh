#!/bin/bash -e

Datasets=('30_personae','196_autoMpg','185_baseball','26_radon_seed','38_sick','4550_miceProtein','LL0_207_autoPrice','57_hypothyroid','1491_one_hundred_plants_margin','LL0_acled_reduced','LL0_1100_popularkids')

cd "/src/dataclean/DatacleaningD3MWrapper/"

# create text file to record scores and timing information
touch pipeline_tests/scores.txt
echo "DATASET, SCORE, EXECUTION TIME" >> pipeline_tests/scores.txt

for i in "${Datasets[@]}"; do

    # generate and save pipeline
    python3 "/src/dataclean/DatacleaningD3MWrapper/pipeline.py" $i

    # test and score pipeline    
    start=`date +%s`
    python3 -m d3m runtime -d /datasets/ fit-score -p *.json -i /datasets/seed_datasets_current/$i/TRAIN/dataset_TRAIN/datasetDoc.json -t /datasets/seed_datasets_current/$i/TEST/dataset_TEST/datasetDoc.json -a /datasets/seed_datasets_current/$i/SCORE/dataset_TEST/datasetDoc.json -r /datasets/seed_datasets_current/$i/${i}_problem/problemDoc.json -O ${i}_pipeline_run.yaml -c scores.csv
    end=`date +%s`
    runtime=$((end-start))
    
    IFS=, read col1 score col3 col4 < <(tail -n1 scores.csv)
        echo "$i, $score, $runtime" >> pipeline_tests/scores.txt

    # cleanup temporary file
    mv *.json pipeline_tests/${i}_pipeline.json
    mv ${i}_pipeline_run.yaml pipeline_tests/${i}_pipeline_run.yaml
    cp "/src/dataclean/DatacleaningD3MWrapper/pipeline.py" "/src/dataclean/DatacleaningD3MWrapper/pipeline_tests/${i}_pipeline.py"
    rm *.meta
    rm scores.csv  
done
