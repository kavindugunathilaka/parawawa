"""Content for the two system pages (/systems/<slug>/).
Every claim here is already made elsewhere on the site (models section, FAQ,
articles 2-4). No prices, capacities or specifications are invented.
Edit here, then run: python tools/build.py"""

COMPARE_TABLE = '''
<div class="table-scroll"><table>
  <thead><tr><th>Feature</th><th>Option A &ndash; Gravity-Fed</th><th>Option B &ndash; Pump Seal Type</th></tr></thead>
  <tbody>
    <tr><td><strong>Best for</strong></td><td>Standard ground, normal soil elevation and water table</td><td>High water table, marshy, coastal and flat land</td></tr>
    <tr><td><strong>Discharge</strong></td><td>Natural gravity flow</td><td>Sealed submersible pump lifts clarified water</td></tr>
    <tr><td><strong>Electricity</strong></td><td>0% &ndash; fully passive</td><td>The submersible pump needs electricity</td></tr>
    <tr><td><strong>Power cuts</strong></td><td>Keeps operating</td><td>The pump needs power to discharge</td></tr>
    <tr><td><strong>Treatment</strong></td><td colspan="2">Same patented layer-base biological filtration (Sri Lanka Patent #10848)</td></tr>
    <tr><td><strong>Warranty</strong></td><td colspan="2">10-year written manufacturer warranty on both options</td></tr>
  </tbody>
</table></div>
'''

SYSTEMS = [
    {
        'slug': 'gravity-fed-bio-septic-tank',
        'name': 'Option A: 100% Gravity-Fed Bio Septic Tank',
        'productName': 'Parawewa Option A Gravity-Fed Bio Septic Tank',
        'metaTitle': 'Gravity-Fed Bio Septic Tank, 0% Electricity | Parawewa',
        'metaDescription': 'Parawewa Option A is a patented gravity-fed bio septic tank for normal ground: no electricity, keeps working in power cuts, 10-year written warranty.',
        'keywords': 'gravity fed septic tank Sri Lanka, no electricity septic tank, bio septic tank, Parawewa Option A',
        'eyebrow': 'OPTION A • STANDARD GROUND',
        'lede': 'A patented layer-base system that treats household and commercial wastewater by natural gravity flow, with no electricity needed for standard ground conditions.',
        'img': 'assets/real_app_apartment.jpg',
        'imgAlt': 'Parawewa tank installation in a residential garden',
        'published': '2026-10-07',
        'modified': '2026-10-07',
        'related': [4, 2, 5],
        'other': 'pump-seal-type-bio-septic-tank',
        'facts': [
            ('Best for', 'Standard ground with a normal water table'),
            ('Electricity', '0% &ndash; passive gravity flow'),
            ('During power cuts', 'Keeps operating'),
            ('Warranty', '10-year written guarantee'),
            ('Technology', 'Patented layer-base system, Sri Lanka Patent #10848'),
            ('Gully bowser emptying', 'Not required'),
        ],
        'body': '''
<h2>What is Option A?</h2>
<p>Option A is the standard Parawewa configuration: a patented, layer-base bio septic tank that treats wastewater by natural gravity flow. Effluent passes through four layers of biological filter media with no blower, no pump and no electricity, which keeps running costs to a minimum wherever the ground allows it.</p>

<h2>How Option A treats wastewater</h2>
<p>The design copies the way a natural riverbed or wetland filters organic matter. Instead of an oxygen-starved pit where sludge simply builds up, wastewater moves through distinct biological stages populated by naturally occurring bacteria:</p>
<ol>
  <li><strong>Primary separation.</strong> Heavier solids and grease settle out as wastewater enters, reducing the load on the biological stages that follow.</li>
  <li><strong>Aerobic microbial digestion.</strong> Oxygen-favouring bacteria colonise the layer-base media and digest organic sludge, converting it into liquid and gas rather than letting it accumulate.</li>
  <li><strong>Layer-base filtration.</strong> Effluent rises through filter media layers that trap fine particles and continue the bacterial treatment.</li>
  <li><strong>Clean, low-noise outflow.</strong> Clarified, largely odourless water discharges to gardens or drains.</li>
</ol>
<p>Read the full explanation in <a href="/articles/how-layer-base-bio-septic-tank-works/">How a layer-base bio septic tank works without electricity</a>.</p>

<h2>Why choose Option A</h2>
<ul>
  <li><strong>0% electricity.</strong> There is no blower or pump, so the system adds nothing to your power bill.</li>
  <li><strong>Operational during power cuts.</strong> Because the flow is passive, a power cut does not stop treatment. Imported mechanical plants rely on a blower running 24/7; see <a href="/articles/parawewa-vs-mechanical-stp-option-a-option-b/">Parawewa vs mechanical STPs</a>.</li>
  <li><strong>No mechanical parts to service or replace.</strong> There is nothing in Option A that needs routine mechanical servicing.</li>
  <li><strong>No gully bowser emptying.</strong> Continuous biological digestion is designed to avoid the recurring suction-truck visits that a concrete pit needs.</li>
  <li><strong>10-year written warranty.</strong> The manufacturer guarantee covers structural tank integrity, chamber sealing and multi-stage biological filtration performance.</li>
  <li><strong>CEA-oriented performance.</strong> Effluent is laboratory-tested against Central Environmental Authority discharge guidelines (BOD and COD limits).</li>
</ul>

<h2>Who Option A suits</h2>
<p>Option A is intended for standard inland building plots with normal soil elevation and standard ground water levels. It is used for single and multi-storey houses, offices and commercial buildings, hotels, housing schemes and factories. Where reliable running costs and power-cut resilience matter, the zero-electricity design is a clear advantage.</p>

<h2>When Option A is not the right choice</h2>
<p>Gravity discharge only works where the ground allows water to flow away naturally. On high water table land, marshy plots, coastal sites and flat low-lying land, the better fit is <a href="/systems/pump-seal-type-bio-septic-tank/">Option B, the sealed submersible pump seal type</a>. A free site inspection confirms which option suits your plot.</p>

<h2>Option A or Option B?</h2>
''' + COMPARE_TABLE,
        'faqs': [
            ('Does Option A need electricity?', 'No. Option A operates on passive natural gravity flow with 0% electricity, which suits standard ground levels.'),
            ('What happens to Option A during a power cut?', 'Nothing changes. Option A is fully passive, so a power cut does not stop treatment, unlike mechanical plants that depend on a continuously running blower.'),
            ('Can Option A be used on high water table land?', 'Option A is designed for standard ground levels. For high groundwater table land, wetlands and coastal soils, Parawewa recommends Option B, the submersible pump seal type.'),
            ('What does the 10-year warranty cover?', 'Parawewa issues a 10-year written manufacturer guarantee certificate covering structural tank integrity, chamber sealing and multi-stage biological layer filtration performance.'),
            ('What size tank does my property need?', 'Capacity depends on the property type and the number of occupants. Use the tank sizer on the home page for an approximate estimate, then request a free site inspection for an exact recommendation and quote.'),
        ],
    },
    {
        'slug': 'pump-seal-type-bio-septic-tank',
        'name': 'Option B: Submersible Pump Seal Type Bio Septic Tank',
        'productName': 'Parawewa Option B Submersible Pump Seal Type Bio Septic Tank',
        'metaTitle': 'Pump Seal Type Septic Tank for High Water Table | Parawewa',
        'metaDescription': 'Parawewa Option B: a sealed submersible pump bio septic tank for high water table, marshy and coastal land in Sri Lanka. 10-year written warranty.',
        'keywords': 'high water table septic tank, submersible pump septic tank Sri Lanka, marshy land septic, Parawewa Option B',
        'eyebrow': 'OPTION B • HIGH WATER TABLE',
        'lede': 'Engineered for high groundwater table land where gravity discharge is not possible: a hermetically sealed composite body with a heavy-duty submersible effluent pump.',
        'img': 'assets/real_app_house.jpg',
        'imgAlt': 'Parawewa tank covers installed beside a building in Sri Lanka',
        'published': '2026-10-07',
        'modified': '2026-10-07',
        'related': [3, 9, 2],
        'other': 'gravity-fed-bio-septic-tank',
        'facts': [
            ('Best for', 'High water table, marshy, coastal and flat land'),
            ('Body', 'Hermetically sealed composite shell'),
            ('Pump', 'Heavy-duty submersible effluent pump'),
            ('Discharge', 'Clarified water pumped to turf, drains or a soakage point'),
            ('Warranty', '10-year written guarantee'),
            ('Technology', 'Patented layer-base system, Sri Lanka Patent #10848'),
        ],
        'body': '''
<h2>What is Option B?</h2>
<p>Option B is the Parawewa configuration for sites where natural gravity discharge is restricted. It uses the same patented layer-base biological treatment as Option A, in a hermetically sealed composite body, and adds a heavy-duty submersible pump that lifts the clarified water to where it can be discharged safely.</p>

<h2>Why high water table land needs a different design</h2>
<p>In low-lying coastal and wetland areas, the ground is saturated for much of the year, and heavy monsoon rain raises the water table further. Standard concrete rings were never designed for that:</p>
<ul>
  <li>Porous, jointed concrete can take in groundwater and fill up shortly after installation.</li>
  <li>Hydrostatic pressure pushing up from below can shift or float a tank, a problem known locally as &ldquo;tank floating&rdquo;.</li>
  <li>On flat or low plots there is no fall for effluent to leave the tank by gravity.</li>
</ul>
<p>See the full engineering guide: <a href="/articles/bio-septic-tank-high-water-table-sri-lanka/">Installing bio septic tanks in high water table lands</a>.</p>

<h2>How Option B is engineered for these sites</h2>
<ul>
  <li><strong>Sealed composite shell.</strong> A non-porous synthetic wall, rather than jointed concrete, prevents inward water seepage and flood backflow, even when the tank sits below the local water table.</li>
  <li><strong>Submersible effluent pump.</strong> A heavy-duty sealed pump lifts clarified effluent to shallow soakage or garden turf where gravity discharge is not possible.</li>
  <li><strong>Shallow, wide geometry.</strong> Wide, shallow tank geometry avoids deep excavation into saturated ground, reducing excavation risk and dewatering cost.</li>
  <li><strong>Anti-buoyancy anchoring.</strong> The installation is anchored and ballasted to resist uplift from groundwater pressure.</li>
</ul>

<h2>Where Option B is used</h2>
<p>Option B is specified for high groundwater table lands, marshy wetlands, coastal properties and flat elevations, including areas such as Piliyandala, Wattala, Ja-Ela, Negombo and Galle. Parawewa&rsquo;s head office is in Piliyandala, itself a low-lying area, so these are conditions the team works with locally.</p>

<h2>Warranty and treatment performance</h2>
<p>Option B carries the same 10-year written manufacturer warranty as Option A, covering structural tank integrity, chamber sealing and multi-stage biological layer filtration performance. The biological treatment is the patented Parawewa layer-base process (Sri Lanka Patent #10848), with effluent laboratory-tested against CEA discharge guidelines.</p>

<h2>Option A or Option B?</h2>
<p>If your ground is standard and your water table is normal, <a href="/systems/gravity-fed-bio-septic-tank/">Option A (gravity-fed)</a> avoids the pump and uses no electricity. If your site is waterlogged, coastal or flat, Option B is the right fit. A free site inspection confirms which applies.</p>
''' + COMPARE_TABLE,
        'faqs': [
            ('Can Parawewa be installed in high water table and marshy land?', 'Yes. Option B is engineered for high groundwater tables, wetlands and coastal soils such as Piliyandala, Wattala, Ja-Ela, Negombo and Galle. The hermetically sealed composite body prevents inward water seepage and flood backflow.'),
            ('Does Option B use electricity?', 'Yes. The sealed submersible pump uses electricity to lift clarified water to the discharge point. Option A, the gravity-fed model, uses no electricity and is the choice for standard ground.'),
            ('Will the tank float in waterlogged ground?', 'The installation is anchored and ballasted to resist uplift from groundwater pressure, and the tank uses a shallow, wide geometry that avoids deep excavation into saturated soil.'),
            ('What is the difference between Option A and Option B?', 'Option A operates on passive gravity flow with 0% electricity and suits standard ground levels. Option B uses a sealed submersible pump and suits high water table land where gravity discharge is restricted. Both use the same patented layer-base treatment and carry a 10-year written warranty.'),
            ('What does the 10-year warranty cover?', 'Parawewa issues a 10-year written manufacturer guarantee certificate covering structural tank integrity, chamber sealing and multi-stage biological layer filtration performance.'),
        ],
    },
]
