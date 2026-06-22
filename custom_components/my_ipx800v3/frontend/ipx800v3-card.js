/**
 * IPX800 V3 Lovelace Card
 * A synthetic and dense dashboard card for GCE IPX800 V3 integrations.
 */

// We can load LitElement from the Home Assistant frontend helper if available,
// otherwise fall back to a public CDN.
const LitElement = Object.getPrototypeOf(customElements.get("ha-panel-lovelace") || HTMLElement);
const { html, css } = LitElement.prototype;

class IPX800V3Card extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object }
    };
  }

  static get styles() {
    return css`
      :host {
        display: block;
      }
      ha-card {
        background: var(--ha-card-background, var(--card-background-color, #1e1e2e));
        border-radius: var(--ha-card-border-radius, 12px);
        border: 1px solid var(--ha-card-border-color, var(--divider-color, #313244));
        box-shadow: var(--ha-card-box-shadow, none);
        padding: 16px;
        color: var(--primary-text-color, #cdd6f4);
        font-family: var(--paper-font-body1_-_font-family, sans-serif);
      }
      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 10px;
        margin-bottom: 12px;
      }
      .card-header .title {
        font-size: 1.2em;
        font-weight: 500;
        display: flex;
        align-items: center;
        gap: 8px;
      }
      .card-header .status {
        display: flex;
        align-items: center;
        gap: 6px;
        font-size: 0.85em;
        font-weight: 500;
      }
      .status.online {
        color: #2ecc71;
      }
      .status.offline {
        color: #e74c3c;
      }
      .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: currentColor;
        box-shadow: 0 0 6px currentColor;
      }
      .section-title {
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--secondary-text-color, #bac2de);
        margin: 14px 0 8px 0;
        font-weight: 600;
      }
      .grid {
        display: grid;
        gap: 8px;
        margin-bottom: 12px;
      }
      /* Relay Styles */
      .relay-grid {
        grid-template-columns: repeat(var(--relay-columns, 4), 1fr);
      }
      .relay-btn {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 6px;
        padding: 10px 6px;
        text-align: center;
        cursor: pointer;
        font-size: 0.85em;
        font-weight: 500;
        transition: all 0.2s ease-in-out;
        user-select: none;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }
      .relay-btn:hover {
        background: rgba(255, 255, 255, 0.08);
        border-color: rgba(255, 255, 255, 0.2);
      }
      .relay-btn.active {
        background: rgba(46, 204, 113, 0.15);
        border-color: #2ecc71;
        color: #2ecc71;
        box-shadow: 0 0 8px rgba(46, 204, 113, 0.15);
      }
      /* Input Styles */
      .input-grid {
        grid-template-columns: repeat(var(--input-columns, 4), 1fr);
      }
      .input-indicator {
        display: flex;
        align-items: center;
        gap: 8px;
        background: rgba(0, 0, 0, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.03);
        padding: 8px;
        border-radius: 6px;
        font-size: 0.85em;
        overflow: hidden;
        white-space: nowrap;
        text-overflow: ellipsis;
      }
      .led {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: rgba(255, 255, 255, 0.15);
        flex-shrink: 0;
        transition: all 0.3s ease;
      }
      .led.active {
        background-color: #f1c40f;
        box-shadow: 0 0 8px #f1c40f;
      }
      /* Analog Styles */
      .analog-grid {
        grid-template-columns: repeat(var(--analog-columns, 2), 1fr);
        gap: 10px;
      }
      .analog-card {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        gap: 10px;
      }
      .analog-icon {
        color: var(--paper-item-icon-color, #3498db);
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(52, 152, 219, 0.1);
        padding: 8px;
        border-radius: 50%;
      }
      .analog-info {
        display: flex;
        flex-direction: column;
      }
      .analog-label {
        font-size: 0.75em;
        color: var(--secondary-text-color, #bac2de);
      }
      .analog-value {
        font-size: 1.05em;
        font-weight: 600;
      }
      /* Counter Styles */
      .counter-container {
        display: flex;
        flex-direction: column;
        gap: 6px;
      }
      .counter-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.05);
        padding: 8px 12px;
        border-radius: 6px;
      }
      .counter-name {
        font-size: 0.9em;
      }
      .counter-value {
        font-weight: 600;
        font-size: 0.95em;
        margin-left: 4px;
        color: var(--accent-color, #ff007f);
      }
      .counter-actions {
        display: flex;
        gap: 4px;
      }
      .counter-actions mwc-button {
        --mdc-theme-primary: var(--primary-text-color);
      }
      .counter-btn {
        background: rgba(255, 255, 255, 0.08);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 4px;
        color: var(--primary-text-color);
        cursor: pointer;
        padding: 4px 10px;
        font-size: 0.85em;
        font-weight: bold;
        transition: background 0.1s ease;
      }
      .counter-btn:hover {
        background: rgba(255, 255, 255, 0.15);
      }
      .counter-btn:active {
        background: rgba(255, 255, 255, 0.25);
      }
    `;
  }

  render() {
    if (!this.hass || !this.config) return html``;

    // Retrieve and filter entities containing attributes.ipx_key
    const allIpxEntities = Object.keys(this.hass.states)
      .map(id => this.hass.states[id])
      .filter(stateObj => stateObj.attributes && stateObj.attributes.ipx_key !== undefined);

    // Apply device filter if configured
    const filter = this.config.device_filter ? this.config.device_filter.toLowerCase() : '';
    const entities = allIpxEntities.filter(stateObj => {
      if (!filter) return true;
      return stateObj.entity_id.toLowerCase().includes(filter) ||
             (stateObj.attributes.friendly_name && stateObj.attributes.friendly_name.toLowerCase().includes(filter));
    });

    // Group entities by type/platform
    const relays = entities.filter(e => e.entity_id.startsWith('switch.'));

    // Sort relays by ipx_key numerical suffix so they display in order (led0, led1, led2...)
    relays.sort((a, b) => this._sortIpxKeys(a.attributes.ipx_key, b.attributes.ipx_key));

    const inputs = entities.filter(e => e.entity_id.startsWith('binary_sensor.') && e.attributes.ipx_key.startsWith('btn'));
    inputs.sort((a, b) => this._sortIpxKeys(a.attributes.ipx_key, b.attributes.ipx_key));

    const analogs = entities.filter(e => e.entity_id.startsWith('sensor.') && e.attributes.ipx_key.startsWith('analog'));
    analogs.sort((a, b) => this._sortIpxKeys(a.attributes.ipx_key, b.attributes.ipx_key));

    const counters = entities.filter(e => e.entity_id.startsWith('sensor.') && e.attributes.ipx_key.startsWith('count'));
    counters.sort((a, b) => this._sortIpxKeys(a.attributes.ipx_key, b.attributes.ipx_key));

    // Connection sensor
    const connectionEntity = entities.find(e => e.attributes.ipx_key === 'api_connectivity');
    const isOnline = connectionEntity ? connectionEntity.state === 'on' : true;
    const statusText = connectionEntity ? (isOnline ? "Online" : "Offline") : "Connected";

    // Column overrides from configuration
    const relayColumns = this.config.relay_columns || 4;
    const inputColumns = this.config.input_columns || 4;
    const analogColumns = this.config.analog_columns || 2;

    const cardTitle = this.config.title || (connectionEntity?.attributes.friendly_name ? connectionEntity.attributes.friendly_name.replace(" API connectivity", "") : "IPX800 V3 Panel");

    return html`
      <ha-card style="--relay-columns: ${relayColumns}; --input-columns: ${inputColumns}; --analog-columns: ${analogColumns};">
        <div class="card-header">
          <div class="title">
            <ha-icon icon="mdi:ip-network"></ha-icon>
            <span>${cardTitle}</span>
          </div>
          <div class="status ${isOnline ? 'online' : 'offline'}">
            <span class="status-dot"></span>
            <span>${statusText}</span>
          </div>
        </div>

        <!-- Relays (Outputs) Grid -->
        ${relays.length > 0 ? html`
          <div class="section-title">Relays (Outputs)</div>
          <div class="grid relay-grid">
            ${relays.map(stateObj => {
              const isOn = stateObj.state === 'on';
              const name = this._cleanEntityName(stateObj, 'relay');
              return html`
                <div
                  class="relay-btn ${isOn ? 'active' : ''}"
                  title="${stateObj.entity_id}"
                  @click="${() => this._toggleSwitch(stateObj.entity_id)}"
                >
                  ${name}
                </div>
              `;
            })}
          </div>
        ` : ''}

        <!-- Digital Inputs Grid -->
        ${inputs.length > 0 ? html`
          <div class="section-title">Digital Inputs</div>
          <div class="grid input-grid">
            ${inputs.map(stateObj => {
              const isOn = stateObj.state === 'on';
              const name = this._cleanEntityName(stateObj, 'input');
              return html`
                <div class="input-indicator" title="${stateObj.entity_id}">
                  <span class="led ${isOn ? 'active' : ''}"></span>
                  <span>${name}</span>
                </div>
              `;
            })}
          </div>
        ` : ''}

        <!-- Analog Sensors Grid -->
        ${analogs.length > 0 ? html`
          <div class="section-title">Analog Inputs</div>
          <div class="grid analog-grid">
            ${analogs.map(stateObj => {
              const val = stateObj.state;
              const unit = stateObj.attributes.unit_of_measurement || '';
              const name = this._cleanEntityName(stateObj, 'analog');
              const deviceClass = stateObj.attributes.device_class;
              const icon = this._getAnalogIcon(deviceClass);
              return html`
                <div class="analog-card" title="${stateObj.entity_id}">
                  <div class="analog-icon">
                    <ha-icon icon="${icon}"></ha-icon>
                  </div>
                  <div class="analog-info">
                    <span class="analog-label">${name}</span>
                    <span class="analog-value">${val} ${unit}</span>
                  </div>
                </div>
              `;
            })}
          </div>
        ` : ''}

        <!-- Pulse Counters Stack -->
        ${counters.length > 0 ? html`
          <div class="section-title">Counters</div>
          <div class="counter-container">
            ${counters.map(stateObj => {
              const val = stateObj.state;
              const name = this._cleanEntityName(stateObj, 'counter');
              return html`
                <div class="counter-row" title="${stateObj.entity_id}">
                  <span class="counter-name">
                    ${name}: <span class="counter-value">${val}</span>
                  </span>
                  <div class="counter-actions">
                    <button class="counter-btn" @click="${() => this._adjustCounter(stateObj.entity_id, -10)}">-10</button>
                    <button class="counter-btn" @click="${() => this._adjustCounter(stateObj.entity_id, -1)}">-1</button>
                    <button class="counter-btn" @click="${() => this._adjustCounter(stateObj.entity_id, 1)}">+1</button>
                    <button class="counter-btn" @click="${() => this._adjustCounter(stateObj.entity_id, 10)}">+10</button>
                  </div>
                </div>
              `;
            })}
          </div>
        ` : ''}
      </ha-card>
    `;
  }

  _sortIpxKeys(keyA, keyB) {
    const numA = parseInt(keyA.replace(/^\D+/g, ''), 10);
    const numB = parseInt(keyB.replace(/^\D+/g, ''), 10);
    return numA - numB;
  }

  _cleanEntityName(stateObj, type) {
    let name = stateObj.attributes.friendly_name || '';
    if (!name) {
      const parts = stateObj.entity_id.split('.');
      return parts[parts.length - 1];
    }
    // Remove common prefix like "IPX800" or "My IPX800 V3" to keep it dense
    name = name.replace(/^My IPX800 V3\s+/i, '');
    name = name.replace(/^IPX800\s+/i, '');
    return name;
  }

  _getAnalogIcon(deviceClass) {
    switch (deviceClass) {
      case 'temperature':
        return 'mdi:thermometer';
      case 'illuminance':
        return 'mdi:weather-sunny';
      case 'humidity':
        return 'mdi:water-percent';
      case 'current':
        return 'mdi:flash';
      case 'voltage':
        return 'mdi:sine-wave';
      case 'ph':
        return 'mdi:ph';
      default:
        return 'mdi:gauge';
    }
  }

  _toggleSwitch(entityId) {
    this.hass.callService('switch', 'toggle', { entity_id: entityId });
  }

  _adjustCounter(entityId, offset) {
    this.hass.callService('my_ipx800v3', 'adjust_counter_value', {
      entity_id: entityId,
      offset: offset
    });
  }

  setConfig(config) {
    this.config = config;
  }

  getCardSize() {
    return 3;
  }

  static getConfigElement() {
    return document.createElement("ipx800v3-card-editor");
  }
}

/**
 * UI Editor for IPX800 V3 Card
 */
class IPX800V3CardEditor extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      _config: { type: Object },
    };
  }

  setConfig(config) {
    this._config = config;
  }

  render() {
    if (!this.hass || !this._config) {
      return html``;
    }

    // Définition du schéma de configuration pour générer le formulaire automatiquement
    const schema = [
      {
        name: "title",
        selector: { text: {} }
      },
      {
        name: "device_filter",
        selector: { text: {} }
      },
      {
        name: "",
        type: "grid",
        schema: [
          { name: "relay_columns", selector: { number: { min: 1, max: 8, mode: "box" } } },
          { name: "input_columns", selector: { number: { min: 1, max: 8, mode: "box" } } },
          { name: "analog_columns", selector: { number: { min: 1, max: 8, mode: "box" } } }
        ]
      }
    ];

    return html`
      <ha-form
        .hass=${this.hass}
        .data=${this._config}
        .schema=${schema}
        .computeLabel=${this._computeLabel}
        @value-changed=${this._onValueChanged}
      ></ha-form>
    `;
  }

  // Fonction pour traduire/personnaliser les labels des champs
  _computeLabel(schema) {
    const labels = {
      title: "Titre de la carte (Optionnel)",
      device_filter: "Filtre d'appareil (Ex: ipx800_1)",
      relay_columns: "Colonnes Relais",
      input_columns: "Colonnes Entrées",
      analog_columns: "Colonnes Analogiques"
    };
    return labels[schema.name] || schema.name;
  }

  // Se déclenche à chaque modification d'un champ par l'utilisateur
  _onValueChanged(ev) {
    if (!this._config || !this.hass) {
      return;
    }

    // On diffuse l'événement 'config-changed' pour que Lovelace mette à jour le YAML en arrière-plan
    const event = new CustomEvent("config-changed", {
      detail: { config: ev.detail.value },
      bubbles: true,
      composed: true,
    });
    this.dispatchEvent(event);
  }
}

customElements.define('ipx800v3-card', IPX800V3Card);
customElements.define("ipx800v3-card-editor", IPX800V3CardEditor);

// Configure card list to make it discoverable in the Lovelace card picker
window.customCards = window.customCards || [];
window.customCards.push({
  type: 'ipx800v3-card',
  name: 'IPX800 V3 Card',
  description: 'A dense synthetic card displaying Relays, Digital Inputs, Analogs, and Counters for IPX800 V3 custom integration.',
  preview: true,
  documentationURL: 'https://github.com/amg0/ha_ipx800v3',

  // suggest a card to the user if the entity is from the IPX800 integration
  getEntitySuggestion: (hass, entityId) => {
    const entityReg = hass.entities[entityId];

    // check entity 's platform is this integration IPX800V3
    if (!entityReg || entityReg.platform !== "my_ipx800v3") {
      return null;
    }

    return {
      config: { type: "custom:ipx800v3-card" },
    };
  },
});
