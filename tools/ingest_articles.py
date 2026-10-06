"""One-time ingest: pull the 20 articles out of app.js into content/articles.json
(the single source of truth), adding SEO fields. After this runs, edit
content/articles.json and run tools/build_articles.py to regenerate the pages."""
import json, subprocess, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

node_src = r"""
const fs=require('fs');const src=fs.readFileSync('app.js','utf8');
const a=src.indexOf('const articlesData = {');const b=src.indexOf('// --- Dynamic Toggle for Homepage Articles Grid');
const data=eval('('+src.slice(a+'const articlesData = '.length,b).trim().replace(/;\s*$/,'')+')');
process.stdout.write(JSON.stringify(data));
"""
raw = subprocess.check_output(['node', '-e', node_src])
data = json.loads(raw.decode('utf-8'))

SEO = {
 '1': ('septic-tank-leaking-groundwater-sri-lanka', '5 Signs a Septic Tank Is Leaking Groundwater | Parawewa', "Learn the 5 signs your septic tank is leaking groundwater in Sri Lanka's monsoon, and how a sealed Parawewa bio tank protects your drinking water.", 'septic tank leaking, groundwater contamination Sri Lanka, well water safety, Parawewa', 'WATER SAFETY', [3, 9, 17]),
 '2': ('parawewa-vs-mechanical-stp-option-a-option-b', 'Parawewa vs Mechanical STP: Option A vs Option B', 'Compare 24/7 electric blower running costs of mechanical STPs with Parawewa Option A (gravity, no electricity) and Option B (sealed pump seal type).', 'mechanical STP Sri Lanka, septic tank electricity, gravity septic tank, pump seal type septic', 'COST SAVINGS', [7, 4, 5]),
 '3': ('bio-septic-tank-high-water-table-sri-lanka', 'Bio Septic Tanks for High Water Table Land | Parawewa', 'Engineering guide to installing leak-proof bio septic systems in high water table, coastal and marshy soils like Piliyandala, Wattala and Negombo.', 'high water table septic tank, marshy land construction Sri Lanka, Piliyandala septic system', 'HIGH WATER TABLE LANDS', [9, 1, 15]),
 '4': ('how-layer-base-bio-septic-tank-works', 'How a Layer-Base Bio Septic Tank Works Without Power', 'Explore the 4-stage natural biological filtration in a Parawewa layer-base bio septic tank, where beneficial microbes digest sludge into clean water.', 'how bio septic tank works, layer-base septic tank, biological filtration, aerobic digestion', 'BIOLOGICAL SCIENCE', [5, 2, 6]),
 '5': ('gully-bowser-emptying-not-needed-bio-septic', "Why Gully Bowser Emptying Isn't Needed | Parawewa", 'See how continuous aerobic digestion in a Parawewa bio septic tank reduces sludge build-up, so repeated gully bowser suction visits are not needed.', 'gully bowser, septic tank emptying Sri Lanka, maintenance free septic tank, sludge digestion', 'MAINTENANCE FREE', [4, 16, 7]),
 '6': ('cea-compliance-septic-tank-sri-lanka', 'CEA Standards for Septic Tanks in Sri Lanka | Parawewa', "Understand BOD and COD discharge standards in Sri Lanka and how a Parawewa bio septic system supports Central Environmental Authority (CEA) compliance.", 'CEA septic tank requirements, BOD COD discharge standards Sri Lanka, environmental protection license', 'CEA COMPLIANCE', [20, 19, 13]),
 '7': ('concrete-septic-pit-vs-parawewa-10-year-cost', '10-Year Cost: Concrete Septic Pit vs Parawewa Bio Tank', 'A 10-year cost comparison of a traditional concrete septic pit and a Parawewa bio tank, covering gully bowser fees, power bills and repairs.', 'septic tank cost Sri Lanka, concrete septic pit vs bio tank, 10-year septic cost', 'FINANCIAL ANALYSIS', [2, 11, 5]),
 '8': ('bio-septic-tank-hotels-eco-resorts-sri-lanka', 'Bio Septic Tanks for Hotels & Eco-Resorts in Sri Lanka', 'How odour-free bio septic systems suit hotels and eco-resorts in Bentota, Ella and Sigiriya, including water recycling for garden lawns.', 'hotel septic tank Sri Lanka, eco resort wastewater, Bentota Ella Sigiriya, water recycling', 'HOTELS & RESORTS', [13, 14, 19]),
 '9': ('monsoon-flooding-household-sewage-sri-lanka', 'How Monsoons Affect Household Sewage Systems | Parawewa', 'Heavy monsoon flooding can make traditional septic tanks back up into bathrooms. Learn how sealed bio tanks keep homes hygienic during floods.', 'monsoon flooding septic tank, flood septic backup Sri Lanka, non-return bio tank', 'MONSOONS & CLIMATE', [3, 1, 18]),
 '10': ('sri-lanka-patent-10848-parawewa-story', 'Sri Lanka Patent #10848: The Story of Parawewa', 'How Mr. Dharmakeerthi Mannage created the Parawewa layer-base bio septic system in 1996 and won the 2018 Presidential Innovation Award.', 'Sri Lanka patent 10848, Parawewa history, Presidential Innovation Award 2018, Sri Lankan inventor', 'PATENT & HISTORY', [4, 6, 19]),
 '11': ('septic-tank-installation-cost-sri-lanka', 'Septic Tank Installation Cost in Sri Lanka | Parawewa', 'What drives septic tank pricing in Sri Lanka, and how Option A and Option B installations compare on total cost, not just the quote.', 'septic tank price Sri Lanka, septic tank installation cost, bio septic tank price', 'PRICING GUIDE', [7, 15, 12]),
 '12': ('septic-tank-vs-soakage-pit-sri-lanka', 'Septic Tank vs Soakage Pit: Which Do You Need?', 'Septic tanks and soakage pits solve different problems. Learn how each works and why Sri Lankan properties usually need both, not either.', 'septic tank vs soakage pit, soakage pit Sri Lanka, septic tank buyer guide', "BUYER'S GUIDE", [3, 17, 1]),
 '13': ('bio-septic-systems-apartments-condominiums-colombo', 'Bio Septic Systems for Apartments & Condos in Colombo', 'High-occupancy apartment buildings need wastewater systems sized differently from single homes. Here is what developers should plan for.', 'apartment septic system Colombo, condominium wastewater, high occupancy septic tank', 'APARTMENTS & CONDOS', [14, 8, 6]),
 '14': ('wastewater-systems-schools-hospitals-institutions', 'Wastewater Systems for Schools, Hospitals & Institutions', 'Schools, clinics and other institutional buildings have wastewater needs that differ from homes and factories. Here is what to consider.', 'school septic tank, hospital wastewater Sri Lanka, institutional sewage treatment', 'INSTITUTIONAL BUILDINGS', [13, 8, 20]),
 '15': ('when-to-install-septic-tank-new-house-construction', 'When to Install a Septic Tank in a New House Build', 'Installing a septic tank at the wrong stage of construction causes rework. See where it fits in a typical Sri Lankan building timeline.', 'new house septic tank, septic tank installation timeline, house construction Sri Lanka', 'NEW CONSTRUCTION', [11, 3, 12]),
 '16': ('septic-tank-maintenance-checklist-homeowners', 'Septic Tank Maintenance Checklist for Homeowners', "Parawewa is engineered to be maintenance-free, but a few simple habits protect performance over the warranty period. A homeowner's do and don't list.", 'septic tank maintenance, septic tank care tips, maintenance free septic tank Sri Lanka', 'MAINTENANCE', [17, 5, 18]),
 '17': ('common-septic-tank-problems-warning-signs', 'Common Septic Tank Problems and Warning Signs', 'From slow drains to unexpected odours, a practical troubleshooting guide to the most common septic tank warning signs in Sri Lankan homes.', 'septic tank problems, septic tank warning signs, slow drains odour, septic troubleshooting', 'TROUBLESHOOTING', [16, 18, 1]),
 '18': ('septic-system-emergency-backup-what-to-do', 'Septic System Emergency or Backup: What to Do', 'A septic backup is stressful but manageable. A calm, step-by-step guide to what to do, and what to avoid, in the moment.', 'septic backup, septic emergency, sewage overflow what to do', 'EMERGENCY GUIDE', [17, 16, 9]),
 '19': ('bio-septic-systems-protect-wells-waterways-sri-lanka', "How Bio Septic Systems Protect Sri Lanka's Waterways", 'Poorly treated household sewage quietly contaminates wells and waterways in Sri Lanka. Here is the bigger environmental picture and what helps.', 'well water contamination Sri Lanka, waterway pollution sewage, eco friendly septic', 'ENVIRONMENTAL IMPACT', [1, 9, 6]),
 '20': ('septic-tank-regulations-building-permits-sri-lanka', 'Septic Tank Regulations & Building Permits in Sri Lanka', 'New construction in Sri Lanka typically needs local authority approval, and sometimes CEA approval, for sewage disposal. A general overview.', 'septic tank regulations Sri Lanka, building permit sewage, CEA environmental protection license', 'REGULATIONS & PERMITS', [6, 15, 11]),
}

IMG_ALT = {
 'real_app_house.jpg': 'Parawewa tank covers installed beside a building in Sri Lanka',
 'real_diagram.png': 'Treatment tanks and pipework at a Parawewa installation site',
 'real_app_commercial.jpg': 'Parawewa septic tank installed at a commercial property in Sri Lanka',
 'real_cert_presidential.jpg': 'Presidential Innovation Award 2018 certificate awarded to Parawewa',
 'real_patent.jpg': 'Sri Lanka Patent #10848 certificate for the Parawewa layer-base system',
 'real_app_apartment.jpg': 'Parawewa tank installation in a residential garden',
 'real_hero.jpg': 'Parawewa eco bio septic tank system infographic',
 'project1.jpg': 'Illustration of a bio septic tank being lowered into an excavation at a building site',
 'project2.jpg': 'Illustration of a garden water feature supplied with recycled clean water',
}

out = []
for k in sorted(data, key=int):
    d = data[k]
    slug, mt, md, kw, cat, rel = SEO[k]
    assert len(md) <= 160, (k, len(md))
    assert len(mt) <= 62, (k, len(mt), mt)
    fn = os.path.basename(d['img'])
    out.append({
        'id': int(k), 'slug': slug, 'category': cat, 'badge': d['badge'], 'title': d['title'],
        'metaTitle': mt, 'metaDescription': md, 'keywords': kw, 'summary': d['summary'],
        'img': d['img'], 'imgAlt': IMG_ALT[fn], 'readTime': d['readTime'],
        'published': '2026-09-15' if int(k) <= 10 else '2026-09-29',
        'modified': '2026-10-06', 'related': rel, 'content': d['content'],
    })

os.makedirs('content', exist_ok=True)
json.dump(out, open('content/articles.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print('wrote content/articles.json', len(out), 'articles')
