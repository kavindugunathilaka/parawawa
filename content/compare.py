"""Comparison pages (/compare/<slug>/). Statements about aerated package plants summarise
publicly available supplier descriptions (prefabricated FRP unit, aeration by electric air
blowers, compact, quick to install); statements about Parawewa come from the
site's existing content. No brand or competitor is named on the page.
Edit here, then run: python tools/build.py"""

TABLE = '''
<div class="table-scroll"><table>
  <thead><tr><th>Feature</th><th>Parawewa</th><th>Aerated package plant</th></tr></thead>
  <tbody>
    <tr><td><strong>Origin and technology</strong></td><td>Sri Lankan, patented layer-base system (Patent #10848, invented 1996)</td><td>Prefabricated aerated treatment unit</td></tr>
    <tr><td><strong>Tank body</strong></td><td>Hermetically sealed composite body</td><td>Fibre-reinforced plastic (FRP) unit</td></tr>
    <tr><td><strong>How oxygen reaches the bacteria</strong></td><td>Natural, passive aeration built into the tank geometry (Option A)</td><td>Electric air blowers</td></tr>
    <tr><td><strong>Electricity</strong></td><td>Option A: none. Option B: the submersible pump only</td><td>Required for the blowers</td></tr>
    <tr><td><strong>During a power cut</strong></td><td>Option A keeps operating</td><td>Depends on the blower; ask the supplier in writing</td></tr>
    <tr><td><strong>Footprint</strong></td><td>Sized to the site&rsquo;s occupancy; confirmed at inspection</td><td>Compact; usually the smaller footprint</td></tr>
    <tr><td><strong>Installation</strong></td><td>Site-specific installation by the Parawewa team</td><td>Prefabricated, quick to install above or below ground</td></tr>
    <tr><td><strong>High water table</strong></td><td>Option B is engineered for it</td><td>Sealed units are generally suitable; confirm per model</td></tr>
    <tr><td><strong>Warranty</strong></td><td>10-year written manufacturer guarantee</td><td>Varies by supplier; ask for the terms in writing</td></tr>
    <tr><td><strong>Local manufacture</strong></td><td>Manufactured and installed in Sri Lanka by Parawewa</td><td>Check where it is made and what local support exists</td></tr>
  </tbody>
</table></div>
'''

COMPARE = [
    {
        'slug': 'parawewa-vs-aerated-package-plants',
        'name': 'Parawewa vs Aerated Package Plants: Which System Suits Your Property?',
        'crumb': 'Parawewa vs Aerated Package Plants',
        'metaTitle': 'Parawewa vs Aerated Package Treatment Plants',
        'metaDescription': 'Parawewa passive bio septic system vs aerated package treatment plants: electricity, power cuts, high water table, footprint and warranty compared fairly.',
        'keywords': 'aerated package treatment plant Sri Lanka, package sewage treatment plant, prefabricated STP vs septic tank, wastewater treatment plant Sri Lanka',
        'eyebrow': 'SYSTEM COMPARISON',
        'lede': 'Aerated package plants are prefabricated wastewater treatment units that use electric blowers. Here is an even-handed comparison with the Parawewa layer-base bio septic system, including where each one fits best.',
        'img': 'assets/real_app_commercial.jpg',
        'imgAlt': 'Parawewa septic tank installation at a site in Sri Lanka',
        'published': '2026-10-07',
        'modified': '2026-10-07',
        'related': [2, 4, 3],
        'facts': [
            ('Parawewa Option A', 'Passive gravity flow, 0% electricity'),
            ('Parawewa Option B', 'Sealed submersible pump for high water table land'),
            ('Aerated package plant', 'Prefabricated FRP unit aerated by electric blowers'),
            ('Parawewa warranty', '10-year written manufacturer guarantee'),
        ],
        'body': '''
<h2>What is an aerated package treatment plant?</h2>
<p>An aerated package plant is a prefabricated wastewater treatment unit, typically a fibre-reinforced plastic (FRP) tank, that treats wastewater through combined anaerobic and aerobic stages. Suppliers describe these units as compact, factory-built and quick to install above or below ground. The aeration that keeps the bacteria supplied with oxygen comes from electric air blowers.</p>

<h2>What is Parawewa?</h2>
<p>Parawewa is a Sri Lankan layer-base bio septic system, invented in 1996 and protected by Sri Lanka Patent #10848. It comes in two forms: <a href="/systems/gravity-fed-bio-septic-tank/">Option A</a>, a gravity-fed system with no electricity, and <a href="/systems/pump-seal-type-bio-septic-tank/">Option B</a>, a sealed submersible pump seal type for high water table land. Both carry a 10-year written manufacturer warranty.</p>

<h2>The main difference: how oxygen reaches the bacteria</h2>
<p>Aerobic treatment needs oxygen. An aerated package plant supplies it with air blowers, which means electricity is the plant&rsquo;s running input and the blowers are the part that has to keep working. Parawewa&rsquo;s layer-base design uses a naturally aerated, oxygen-present process built into the geometry of the tank, so Option A has no blower and no compressor. Option B adds a pump only to lift clarified water where gravity discharge is not possible.</p>
<p>For a detailed look at that difference with mechanical plants in general, read <a href="/articles/parawewa-vs-mechanical-stp-option-a-option-b/">Parawewa vs mechanical STPs: Option A vs Option B</a>.</p>

<h2>Side-by-side comparison</h2>
''' + TABLE + '''
<h2>Where an aerated package plant may suit you better</h2>
<ul>
  <li><strong>Very limited space.</strong> Prefabricated aerated units are generally the more compact option.</li>
  <li><strong>Above-ground or relocatable installations.</strong> Suppliers describe units that can be placed above ground or moved later.</li>
  <li><strong>Modular capacity.</strong> Some units can be combined to expand capacity.</li>
  <li><strong>Reliable power and a service contract.</strong> If power is dependable and you are comfortable maintaining blowers, the electricity requirement matters less.</li>
</ul>

<h2>Where Parawewa may suit you better</h2>
<ul>
  <li><strong>You want no electricity.</strong> Option A has no blower and no pump, so nothing is added to your power bill.</li>
  <li><strong>Power cuts are a concern.</strong> A passive system keeps operating when the power goes off.</li>
  <li><strong>High water table or marshy land.</strong> Option B is engineered for waterlogged and coastal sites.</li>
  <li><strong>Local manufacture and a long written warranty.</strong> Parawewa manufactures and installs in Sri Lanka and issues a 10-year written guarantee.</li>
  <li><strong>No gully bowser emptying.</strong> Continuous biological digestion is designed to avoid recurring suction-truck visits.</li>
</ul>

<h2>Questions to ask any supplier</h2>
<ol>
  <li>How much electricity does the system use, and what happens during a power cut?</li>
  <li>What does the warranty cover, for how long, and is it in writing?</li>
  <li>Can I see a laboratory test report for the treated water against CEA discharge limits?</li>
  <li>What routine servicing is needed, and who provides spare parts locally?</li>
  <li>How much space does the installation need, and how deep is the excavation?</li>
</ol>
<p>Parawewa&rsquo;s laboratory test report and patent documents are shown in the certificates section of the <a href="/#certificates">home page</a>.</p>

<p><em>Notes about aerated package plants summarise publicly available supplier descriptions. Specifications, electricity use and warranty terms vary by model and manufacturer, so please confirm details with the supplier.</em></p>
''',
        'faqs': [
            ('Is an aerated package plant better than a septic tank?', 'It depends on the site. A conventional concrete septic tank is a simple settling pit. An aerated package plant is a prefabricated unit that uses blowers. Parawewa is neither: it is a patented layer-base bio septic system that treats wastewater through biological filtration, with a gravity-fed option and a pump seal type option.'),
            ('Does an aerated package plant need electricity?', 'According to supplier descriptions, these units use electric air blowers for aeration, and the blowers are their main electricity use.'),
            ('Does Parawewa need electricity?', 'Option A, the gravity-fed model, uses 0% electricity. Option B uses a sealed submersible pump for high water table land, and the pump uses electricity.'),
            ('Can Parawewa be used where the water table is high?', 'Yes. Option B is engineered for high groundwater table land, wetlands and coastal soils, with a hermetically sealed composite body that prevents inward water seepage and flood backflow.'),
            ('What warranty does Parawewa give?', 'Parawewa issues a 10-year written manufacturer guarantee covering structural tank integrity, chamber sealing and multi-stage biological layer filtration performance.'),
        ],
    },
]
