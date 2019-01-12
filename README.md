# logic-module
Perform logic operations. It firstly reads from the knowledge base, a json file, as consciousness. As those kinds of logical operations may have exponential performances, there are only a limited amount of data can be stored in the consciousness, everything else is stored in a more permenant place. Those permenant knowledge will not be logically analyzed one by one. It only supports induction (simple probability) for now. It will derive rules, predicting a condition's probability given another condition. All histories are remembered, and the probability is calculated when use.

Sample knowledge base:
`[
    {"id": 0, 
        "mode": "knowledge", 
        "object": {"lemma": "it"}, 
        "subset": [{"lemma": "be", "dependencies": [
            {"name": "time", "pos tag": "noun", "id": 2}, 
            {"lemma": ".", "pos tag": "punct", "condition": "dependency"}]}], 
        "time": "2018-12-26 18:41:01.712300"}, 
    {"id": 1, 
        "mode": "command", 
        "object": "you", 
        "subset": [{"lemma": "find", "dependencies": [
            {"name": "menu", "pos tag": "noun", "id": 0}]}], 
        "time": "2018-12-26 18:41:01.712300"}, 
    {"id": 2, 
        "mode": "knowledge", 
        "object": {"lemma": "it"}, 
        "subset": [{"lemma": "be", "dependencies": [
            {"name": "time", "pos tag": "noun", "id": 2}, 
            {"lemma": ".", "pos tag": "punct", "condition": "dependency"}]}], 
        "time": "2018-12-27 14:33:10.953144"}, 
    {"id": 3, 
        "mode": "command", 
        "object": "you", 
        "subset": [{"lemma": "find", "dependencies": [{"name": "music", "pos tag": "noun", "id": 3}]}], 
        "time": "2018-12-27 14:33:10.953144"}, 
    {"id": 4, 
        "mode": "knowledge", 
        "object": {"lemma": "it"}, 
        "subset": [{"lemma": "be", "dependencies": [{"name": "time", "pos tag": "noun", "id": 2}, {"lemma": ".", "pos tag": "punct", "condition": "dependency"}]}], 
        "time": "2018-12-27 14:33:21.337621"}, 
    {"id": 5, 
        "mode": "command", 
        "object": "you", 
        "subset": [{"lemma": "find", "dependencies": [{"name": "music", "pos tag": "noun", "id": 3}]}], 
        "time": "2018-12-27 14:33:21.337621"}]`
        
Sample logic base:
`[{"statement": {"mode": "knowledge", "object": {"lemma": "it"}, "subset": [{"lemma": "be", "dependencies": [{"name": "time", "pos tag": "noun", "id": 2}, {"lemma": ".", "pos tag": "punct", "condition": "dependency"}]}]}, "history": [0, 2, 4], "relation list": [{"statement": {"mode": "command", "object": "you", "subset": [{"lemma": "find", "dependencies": [{"name": "menu", "pos tag": "noun", "id": 0}]}]}, "history": [[0, 1]]}, {"statement": {"mode": "command", "object": "you", "subset": [{"lemma": "find", "dependencies": [{"name": "music", "pos tag": "noun", "id": 3}]}]}, "history": [[4, 5], [2, 3]]}]}, {"statement": {"mode": "command", "object": "you", "subset": [{"lemma": "find", "dependencies": [{"name": "menu", "pos tag": "noun", "id": 0}]}]}, "history": [1], "relation list": [{"statement": {"mode": "knowledge", "object": {"lemma": "it"}, "subset": [{"lemma": "be", "dependencies": [{"name": "time", "pos tag": "noun", "id": 2}, {"lemma": ".", "pos tag": "punct", "condition": "dependency"}]}]}, "history": [[1, 0]]}]}, {"statement": {"mode": "command", "object": "you", "subset": [{"lemma": "find", "dependencies": [{"name": "music", "pos tag": "noun", "id": 3}]}]}, "history": [3, 5], "relation list": [{"statement": {"mode": "knowledge", "object": {"lemma": "it"}, "subset": [{"lemma": "be", "dependencies": [{"name": "time", "pos tag": "noun", "id": 2}, {"lemma": ".", "pos tag": "punct", "condition": "dependency"}]}]}, "history": [[5, 4], [3, 2]]}]}]`
