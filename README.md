# Waste Collection Komunala Kranj

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Home Assistant integration for Komunala Kranj waste collection schedule. Get notifications about upcoming waste collection dates and see the schedule in a color-coded dashboard.

## Features

- Shows upcoming waste collection dates
- Color-coded by waste type (Yellow for EMB, Brown for BIO, Green for MKO)
- Sends notifications day before collection at 8 PM
- Easy setup through UI
- Supports multiple waste types:
  - ODPADNA EMBALAŽA (Waste Packaging)
  - BIOLOŠKI ODPADKI (Biological Waste)
  - MEŠANI KOMUNALNI ODPADKI (Mixed Waste)

## Installation

1. Add this repository to HACS as a custom repository:
   - HACS -> Integrations -> Three dots menu -> Custom repositories
   - URL: https://github.com/th0r88/hacs-waste-collection-komunala-kranj
   - Category: Integration

2. Install the integration through HACS
3. Restart Home Assistant
4. Go to Settings -> Devices & Services
5. Click "+ ADD INTEGRATION"
6. Search for "Waste Collection Kranj"
7. Enter your household ID (hsMid)

## List of household IDs (hsMid) - [source](https://www.komunala-kranj.si/ravnanje-z-odpadki/redni-odvoz-odpadkov)

- Urnik 1A: KS Stražišče, KS Gorenja Sava, KS Besnica - (hsMid): **12258984**
- Urnik 1B: KS Orehek-Drulovka, KS Mavčiče, KS Bitnje, KS Žabnica, KS Jošt - (hsMid): **12200404**
- Urnik 2: KS Britof in KS Predoslje - (hsMid): **12201575**
- Urnik 3A:  KS Golnik, KS Goriče, KS Trstenik, KS Struževo, del KS Center, del KS Vodovodni stolp, del KS Zlato polje - (hsMid): **12230630**
- Urnik 3B:  KS Kokrica in KS Tenetiše - (hsMid): **12287577**
- Urnik 4: del KS Huje, del KS Planina, del KS Primskovo - (hsMid): **12233027**
- Urnik 5: del KS Bratov Smuk, del KS Huje, del KS Planina, del KS Primskovo - (hsMid): **12229976**
- Urnik 6: del KS Center – staro mestno jedro - (hsMid): **12229623**
- Urnik 7: del KS Center, del KS Vodovodni stolp, del KS Zlato polje - (hsMid): **12228716**
- Urnik 8: del KS Podblica - (hsMid): **12299486**
- Urnik 9: KS Čirče in KS Hrastje - (hsMid): **12239050**
- Urnik Jezersko - (hsMid): **12318120**
- Urnik Preddvor - (hsMid): **12307217**
- Urnik Šenčur A - (hsMid): **12326572**
- Urnik Šenčur B - (hsMid): **12327820**

## Configuration

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| hsmid | string | yes | - | Your household ID from Komunala Kranj |
| name | string | no | Waste Collection Kranj | Name of the sensor |

## Dashboard Card

1. Install Mushroom through HACS
2. Add this card to your dashboard:

```yaml
type: custom:auto-entities
filter:
  include:
    - entity_id: sensor.waste_collection_komunala_kranj
card:
  type: custom:mushroom-template-card
  alignment: left
  secondary: |
    {% for collection in state_attr('sensor.waste_collection_komunala_kranj', 'collections') %}{% if collection.description == "ODPADNA EMBALAŽA" %}🟡 {{collection.date}} - {{collection.description}}
    {% elif collection.description == "BIOLOŠKI ODPADKI" %}🟤 {{collection.date}} - {{collection.description}}
    {% elif collection.description == "MEŠANI KOMUNALNI ODPADKI" %}🟢 {{collection.date}} - {{collection.description}}
    {% endif %}{% endfor %}
  fill_container: true
  multiline_secondary: true
  card_mod:
    style:
      mushroom-template-card$:
        ". mushroom-template-card-secondary": |
          line-height: 2;
          display: block;