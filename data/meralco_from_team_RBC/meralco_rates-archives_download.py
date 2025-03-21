import os
months = [
    "january",
    "february",
    "march",
    "april",
    "may",
    "june",
    "july",
    "august",
    "september",
    "october",
    "november",
    "december"
]

doctypes = {
    "Typical Consumption Level",
    "Summary Schedule of Rates",
    "Generation"
}

# TODO: years must be adjusted when new data is added
for year in range(2009, 2024+1):
    os.system(f"mkdir {year}")

for i in range(0, 88):
    print(f"FILE: {i}.html")
    html = open(f"{i}.html").read()
    start = html.find("<table")
    start = html.find("<td", start)
    end = html.find("</table>", start)
    end = html.rfind("</td>", start, end) + len("</td>")

    html = html[start:end]
    # print(html[start:end])
    # input()
    for entry in html.split("<tr>"):
        _empty, period, doctype, link = entry.split("<td")
        print(period, doctype,link, sep="\n")

        period_start = period.find('">') + len('">')
        period_end = period.find('</td>', period_start)
        month, year = map(lambda x: x.strip().lower(), period[period_start:period_end].strip().split(" "));

        month = months.index(month) + 1

        doctype_start = doctype.rfind('">') + len('">')
        doctype_end = doctype.rfind('</span>')
        doctype = doctype[doctype_start:doctype_end].strip()

        # HACK: some tables list Typical Consumption Levels. Remove the 's' for consistency
        if (doctype.endswith("Levels")):
            doctype = doctype[:-1]

        link_start = link.find('"https:') + 1
        link_end = link.rfind('.pdf"') + len('.pdf')
        link = link[link_start:link_end]

        filename = f'{month}-{year}_{doctype}.pdf'

        if doctype not in doctypes:
            print(f"WARNING: {filename} from {link} has unknown doctype {doctype}.")

        print(f"OUTPUT: {filename} ({link})")

        os.system(f"wget -O '{year}/{filename}' {link}")
