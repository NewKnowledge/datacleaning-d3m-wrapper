#!/bin/bash -e 

Datasets=('30_personae' '185_baseball' '1491_one_hundred_plants_margin' 'LL0_1100_popularkids' '38_sick' '4550_MiceProtein' '57_hypothyroid' 'LL0_acled_reduced')
Bools=('True' 'False')
cd /primitives/v2019.6.7/Distil/d3m.primitives.feature_selection.rffeatures.Rffeatures/3.1.1/pipelines
mkdir test_pipeline
mkdir best_pipelines

# create text file to record scores and timing information
touch scores.txt
echo "DATASET, SCORE, EXECUTION TIME" >> scores.txt
cd test_pipeline

for i in "${Datasets[@]}"; do

    # generate and save pipeline + metafile
    python3 "/src/dataclean/DatacleaningD3MWrapper/pipeline.py" $i

    # test and score pipeline
    start=`date +%s` 
    python3 -m d3m runtime -d /datasets/ fit-score -m *.meta -p *.json -c scores.csv
    end=`date +%s`
    runtime=$((end-start))

    if [ $runtime -lt 3600 ]; then
    echo "$i took less than 1 hour, evaluating pipeline"
    IFS=, read col1 score col3 col4 < <(tail -n1 scores.csv)
        echo "$i, $score, $runtime" >> ../scores.txt
        cp *.meta ../best_pipelines
        cp *.json ../best_pipelines
    fi

    # cleanup temporary file
    rm *.meta
    rm *.json
    rm scores.csv
done