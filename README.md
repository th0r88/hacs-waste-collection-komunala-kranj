# Waste Collection Kranj

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

## Configuration

| Option | Type | Required | Default | Description |
|--------|------|----------|---------|-------------|
| hsmid | string | yes | - | Your household ID from Komunala Kranj |
| name | string | no | Waste Collection Kranj | Name of the sensor |

## Dashboard Card

After installation, you can add this card to your dashboard:

```yaml
type: custom:auto-entities
filter:
  include:
    - entity_id: sensor.waste_collection_kranj
card:
  type: custom:stack-in-card
  cards:
    - type: markdown
      content: >
        {% set collections = state_attr('sensor.waste_collection_kranj',
        'collections') %}
        {% if collections %}
          {% for collection in collections %}
            {% set color = collection.color %}
            {% set date = collection.date %}
            {% set type = collection.description %}
            <div style="
              padding: 10px;
              margin: 5px;
              background-color: {{ color }};
              border-radius: 5px;
              color: {% if color == '#f9df2e' %}black{% else %}white{% endif %};
            ">
              {{ date }} - {{ type }}
            </div>
          {% endfor %}
        {% else %}
          <div style="padding: 10px; margin: 5px;">
            No upcoming waste collections found
          </div>
        {% endif %}