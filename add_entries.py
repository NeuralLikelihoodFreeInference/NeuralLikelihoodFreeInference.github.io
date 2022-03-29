import json
from dateutil.parser import parse
from datetime import datetime

outfile_name = "index.html"

# Opening JSON file
f = open('entries.json')

# returns JSON object as a dictionary
entries = json.load(f)

# lists of unique items
years_list = []
authors_list = []
target_list = []
nn_list = []
samples_list = []
sequential_list = []

names = ["authors", "target", "nn", "samples", "sequential"]
lists = [authors_list, target_list, nn_list, samples_list, sequential_list]

# Iterating through the json and add things to lists of unique items
for entry in entries:
    # print(entry)

    # extract unique elements in each field
    for name, l in zip(names, lists):
        if not isinstance(entry[name], list):
            if entry[name] not in l: l.append(entry[name])
        else:
            for element in entry[name]:
                if element not in l: l.append(element)

    # extract dates:
    year = parse(entry["date"]).year
    if year not in years_list: years_list.append(year)

authors_list = sorted(authors_list)  # sort it
years_list = sorted(years_list)  # sort it

# print(years_list)
# print(authors_list)
# print(target_list)
# print(nn_list)
# print(samples_list)
# print(sequential_list)

# sort entries according to date:
all_dates = [entry["date"] for entry in entries]
sorted_zipped = sorted(zip(all_dates, entries), key=lambda x: parse(x[0]).date())
# unzip:
sorted_dates = [x[0] for x in sorted_zipped]
entries = [x[1] for x in sorted_zipped]

# --- START WRITING THINGS TO HTML ---

f_out = open(outfile_name, "w")

# write the selectors to the html file:

f_out.write(
    '---\n'
    'layout: default\n'
    '---\n'
    '<div class="row">\n'
    '  <span class="selector">\n'
    '    <span>Authors: </span>\n'
    '    <select id="authorselection" class="selectpicker" multiple data-live-search="true">\n'
)

for author in authors_list:
    f_out.write(f'<option>{author}</option>\n')

f_out.write(
    '    </select>\n'
    '  </span>\n'
    '  <div class="selector">\n'
    '    <span>Year: </span>\n'
    '    <select id="yearselection" class="selectpicker" multiple data-live-search="true">\n'
)
for year in years_list:
    f_out.write(f'<option>{year}</option>\n')
f_out.write(
    '    </select>\n'
    '  </div>\n'
    '  <span class="selector">\n'
    '    <span>Target: </span>\n'
    '    <select id="targetselection" class="selectpicker" multiple data-live-search="true">\n'
)
for target in target_list:
    f_out.write(f'<option>{target}</option>\n')
f_out.write(
    '    </select>\n'
    '  </span>\n'
    '  <span class="selector">\n'
    '    <span>Neural Network: </span>\n'
    '    <select id="nnselection" class="selectpicker" multiple data-live-search="true">\n'
)
for nn in nn_list:
    f_out.write(f'<option>{nn}</option>\n')
f_out.write(
    '    </select>\n'
    '  </span>\n'
    '  <span class="selector">\n'
    '    <span>Samples: </span>\n'
    '    <select id="samplesselection" class="selectpicker" multiple data-live-search="true">\n'
)
for sample in samples_list:
    f_out.write(f'<option>{sample}</option>\n')
f_out.write(
    '</select>\n'
    '  </span>\n'
    '  <span class="selector">\n'
    '    <span>Sequential: </span>\n'
    '    <select id="seqamselection" class="selectpicker" multiple data-live-search="true">\n'
)
for amo in sequential_list:
    f_out.write(f'<option>{amo}</option>\n')
f_out.write(
    '    </select>\n'
    '  </span>\n'
    '</div>\n'
    '{% assign id = 0 %}\n'
    ' <hr/>\n'
)

# add each entry now:

for entry in entries:
    # fix the "others" list: 
    if not isinstance(entry["other"], list):
        entry["other"] = [entry["other"]]
    other_not_empty = len(entry["other"]) > 0

    f_out.write(
        '        <!--Post--------------------------------------------------------------------------------------------------------------------------------------------->\n'
        '{% assign id = id | plus:1 %}\n'
        '<div class="entry">\n'
        '	<div class="row">\n'
        '	  <div class="column1" >\n'
        '{% capture x %}\n'
        f'## {entry["title"]}\n'
        '    {% endcapture %}{{ x | markdownify }}\n'
        '	  </div>\n'
        '	  <div class="column2" >\n'
        '	    <div id="block_container">\n'
        '		<div id="bloc2">\n'
        f' 		<a href="{entry["link"]}" target="_blank" class="btn btn-info" role="button"> Paper </a>\n'
        '		</div>\n'
        '		<div id="bloc3">\n'
        '		     <p>\n'
    )
    if other_not_empty:
        f_out.write(
            '		      <button class="btn btn-primary" type="button" data-toggle="collapse" data-target="#collapse{{ id }}" aria-expanded="false" aria-controls="collapse{{ id }}">\n'
            '				See More\n'
            '		      </button>\n'
        )
    f_out.write(
        '		    </p>\n'
        '		</div>\n'
        '	     </div>\n'
        '	  </div>\n'
        '	</div>\n'
        '	<div class="row">\n'
        '		<div id="bloc2">\n'
        f'          <span class="dates"> {entry["date"]} </span>\n')

    authors_list_string = ''
    for i in range(len(entry["authors"]) - 1):
        authors_list_string += f'{entry["authors"][i]}, '
    authors_list_string += f'{entry["authors"][-1]}'

    f_out.write(f'          <span class="authors"> {authors_list_string} </span>\n'
        '    		</div>\n'
        '	</div>\n'
        '    <div class="row">\n'
        '		<div id="bloc2">\n'
    )
    target_list_string = ''
    if not isinstance(entry["target"], list):
        entry["target"] = [entry["target"]]
    for i in range(len(entry["target"]) - 1):
        target_list_string += f'{entry["target"][i]}, '
    if len(entry["target"]) > 0:
        target_list_string += f'{entry["target"][-1]}'
        f_out.write('	  	<span class="label_first">   Target: 		  </span>\n')
    f_out.write(f'        <span class="target"> 		{target_list_string} 	 </span>\n')

    nn_list_string = ''
    if not isinstance(entry["nn"], list):
        entry["nn"] = [entry["nn"]]
    for i in range(len(entry["nn"]) - 1):
        nn_list_string += f'{entry["nn"][i]}, '
    if len(entry["nn"]) > 0:
        nn_list_string += f'{entry["nn"][-1]}'
        f_out.write('  	<span class="label">   Neural Network: 		  </span>')
    f_out.write(f'        <span class="nn"> 		{nn_list_string} 	 </span>\n')

    samples_list_string = ''
    if not isinstance(entry["samples"], list):
        entry["samples"] = [entry["samples"]]
    for i in range(len(entry["samples"]) - 1):
        samples_list_string += f'{entry["samples"][i]}, '
    if len(entry["samples"]) > 0:
        samples_list_string += f'{entry["samples"][-1]}'
        f_out.write('  	<span class="label">   Samples: 		  </span>')
    f_out.write(        f'        <span class="samples"> 		{samples_list_string} 	 </span>\n')

    sequential_list_string = ''
    if not isinstance(entry["sequential"], list):
        entry["sequential"] = [entry["sequential"]]
    for i in range(len(entry["sequential"]) - 1):
        sequential_list_string += f'{entry["sequential"][i]}, '
    if len(entry["sequential"]) > 0:
        sequential_list_string += f'{entry["sequential"][-1]}'
        f_out.write('  	<span class="label">   Sequential: 		  </span>')
    f_out.write(        f'        <span class="seq_am"> 		{sequential_list_string} 	 </span>\n')

    if "additional_description" in entry:
        f_out.write(
            f'        <span class="additional_description"> 		{entry["additional_description"]} 	 </span>\n')

    f_out.write(
        '    	</div>\n'
        '	</div>\n'
    )
    if other_not_empty:
        f_out.write(
            '<div class="collapse" id="collapse{{ id }}">\n'
            '{% capture x %}\n'
        )
        for element in entry["other"]:
            f_out.write('* ' + element + '\n')
        f_out.write(
            '{% endcapture %}{{ x | markdownify }}\n'
            '</div>\n'
        )
    f_out.write(
        ' <hr/>\n'
        '</div>\n'
        '<!--EndPost--------------------------------------------------------------------------------------------------------------------------------------------->\n'
    )

# Closing file
f.close()
