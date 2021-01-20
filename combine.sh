#!/bin/bash
ls answers | grep answer_0 | sed -e 's/answer_0_//g' | sed -e 's/.html//g' | xargs -I {} sh -c "find answers | grep {} | sed -e 's/$/ .\/answers\/dummy.html/g' | tr '\n' ' ' | xargs cat > ./processed/{}.html"
