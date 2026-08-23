/**
 * IPX800 V3 Lovelace Card - Hybrid Version (PC/Mobile Editor + Cast/Nest Hub Compatible)
 */

// 1. Détection dynamique et sécurisée du prototype LitElement
const getLitElement = () => {
  if (customElements.get("ha-panel-lovelace")) {
    return Object.getPrototypeOf(customElements.get("ha-panel-lovelace"));
  }
  if (customElements.get("hui-view")) {
    return Object.getPrototypeOf(customElements.get("hui-view"));
  }
  if (customElements.get("hc-main")) {
    return Object.getPrototypeOf(customElements.get("hc-main"));
  }
  return HTMLElement;
};

const LitElement = getLitElement();
const html = LitElement.prototype.html || window.litHtml;
const css = LitElement.prototype.css || window.litCss;

const editorTranslations = {
  en: {
    title: "Card Title (Optional)",
    device_filter: "Device Filter (comma-separated, e.g., ipx800_1, ipx800_2)",
    device_exclude: "Device Exclude (comma-separated, e.g., light, temperature)",
    relay_columns: "Relay Columns",
    input_columns: "Input Columns",
    analog_columns: "Analog Columns"
  },
  fr: {
    title: "Titre de la carte (Optionnel)",
    device_filter: "Filtre d'appareil (séparé par des virgules, Ex: ipx800_1, ipx800_2)",
    device_exclude: "Exclusion d'appareil (séparé par des virgules, Ex: light, temperature)",
    relay_columns: "Colonnes Relais",
    input_columns: "Colonnes Entrées",
    analog_columns: "Colonnes Analogiques"
  }
};

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
        font-size: 1em;
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
      .status.online { color: #2ecc71; }
      .status.offline { color: #e74c3c; }
      .status-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background-color: currentColor;
        box-shadow: 0 0 6px currentColor;
      }
      .section-title {
        display: flex;
        align-items: center;
        font-size: 0.8em;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        color: var(--secondary-text-color, #bac2de);
        margin: 18px 0 10px 0;
        font-weight: 600;
      }
      .section-title::after {
        content: "";
        flex: 1;
        height: 1px;
        background-color: var(--divider-color, rgba(255, 255, 255, 0.1));
        margin-left: 12px;
      }
      .grid {
        display: grid;
        gap: 10px;
        margin-bottom: 12px;
      }
      .relay-grid {
        grid-template-columns: repeat(var(--relay-columns, 4), 1fr);
      }
      .relay-btn {
        background: rgba(255, 255, 255, 0.03);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 12px 8px;
        text-align: center;
        cursor: pointer;
        font-size: 0.85em;
        font-weight: 500;
        letter-spacing: 0.3px;
        transition: all 0.25s cubic-bezier(0.4, 0, 0.2, 1);
        user-select: none;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      }
      .relay-btn:hover {
        background: rgba(255, 255, 255, 0.07);
        border-color: rgba(255, 255, 255, 0.15);
        transform: translateY(-1px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
      }
      .relay-btn:active {
        transform: translateY(0);
      }
      .relay-btn.active {
        background: rgba(46, 204, 113, 0.16);
        border-color: rgba(46, 204, 113, 0.6);
        color: #2ecc71;
        font-weight: 600;
        box-shadow: 0 0 10px rgba(46, 204, 113, 0.12), inset 0 0 4px rgba(46, 204, 113, 0.1);
      }
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
        background-color: #2ecc71;
        box-shadow: 0 0 8px #2ecc71;
      }
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
      .counter-name { font-size: 0.9em; }
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

      @media (max-width: 768px) {
        .relay-grid, .input-grid { grid-template-columns: repeat(3, 1fr) !important; }
      }
      @media (max-width: 480px) {
        ha-card { padding: 12px; }
        .relay-grid, .input-grid { grid-template-columns: repeat(2, 1fr) !important; }
        .analog-grid { grid-template-columns: 1fr !important; }
        .counter-row { flex-direction: column; align-items: flex-start; gap: 8px; }
        .counter-actions { width: 100%; justify-content: space-between; }
        .counter-btn { flex: 1; text-align: center; }
      }
    `;
  }

  static getStubConfig() {
    return {
      title: "IPX800 V3 Panel",
      relay_columns: 4,
      input_columns: 4,
      analog_columns: 2
    };
  }

  shouldUpdate(changedProps) {
    // Détection dynamique de l'environnement Cast / Nest Hub
    const isCast = navigator.userAgent.includes("CrKey") || !customElements.get("ha-panel-lovelace");
    if (isCast) return true;

    if (changedProps.has('config')) return true;

    if (changedProps.has('hass')) {
      const oldHass = changedProps.get('hass');
      if (!oldHass) return true;
      if (!this.hass || !this.hass.states) return true;

      for (const entityId in this.hass.states) {
        const stateObj = this.hass.states[entityId];
        if (stateObj && stateObj.attributes && stateObj.attributes.ipx_key !== undefined) {
          if (!oldHass.states || oldHass.states[entityId] !== stateObj) {
            return true;
          }
        }
      }
      return false;
    }
    return true;
  }

  render() {
    if (!this.hass || !this.config) return html``;

    const states = this.hass.states || {};
    const allIpxEntities = Object.keys(states)
      .map(id => states[id])
      .filter(stateObj => stateObj && stateObj.attributes && stateObj.attributes.ipx_key !== undefined);

    let filters = [];
    if (this.config.device_filter) {
      if (Array.isArray(this.config.device_filter)) {
        filters = this.config.device_filter.map(f => String(f).trim().toLowerCase()).filter(f => f !== "");
      } else if (typeof this.config.device_filter === "string") {
        filters = this.config.device_filter.split(",").map(f => f.trim().toLowerCase()).filter(f => f !== "");
      } else {
        filters = [String(this.config.device_filter).trim().toLowerCase()];
      }
    }

    let excludes = [];
    if (this.config.device_exclude) {
      if (Array.isArray(this.config.device_exclude)) {
        excludes = this.config.device_exclude.map(f => String(f).trim().toLowerCase()).filter(f => f !== "");
      } else if (typeof this.config.device_exclude === "string") {
        excludes = this.config.device_exclude.split(",").map(f => f.trim().toLowerCase()).filter(f => f !== "");
      } else {
        excludes = [String(this.config.device_exclude).trim().toLowerCase()];
      }
    }

    const entities = allIpxEntities.filter(stateObj => {
      const entityIdLower = stateObj.entity_id ? stateObj.entity_id.toLowerCase() : "";
      const friendlyNameLower = stateObj.attributes && stateObj.attributes.friendly_name ? stateObj.attributes.friendly_name.toLowerCase() : "";

      if (excludes.length > 0) {
        const matchesExclude = excludes.some(exclude => entityIdLower.includes(exclude) || friendlyNameLower.includes(exclude));
        if (matchesExclude) return false;
      }

      if (filters.length === 0) return true;
      return filters.some(filter => entityIdLower.includes(filter) || friendlyNameLower.includes(filter));
    });

    const relays = entities.filter(e => e.entity_id && e.entity_id.startsWith('switch.'));
    relays.sort((a, b) => this._sortIpxKeys(a.attributes?.ipx_key, b.attributes?.ipx_key));

    const inputs = entities.filter(e => e.entity_id && e.entity_id.startsWith('binary_sensor.') && e.attributes?.ipx_key && String(e.attributes.ipx_key).startsWith('btn'));
    inputs.sort((a, b) => this._sortIpxKeys(a.attributes?.ipx_key, b.attributes?.ipx_key));

    const analogs = entities.filter(e => e.entity_id && e.entity_id.startsWith('sensor.') && e.attributes?.ipx_key && String(e.attributes.ipx_key).startsWith('analog'));
    analogs.sort((a, b) => this._sortIpxKeys(a.attributes?.ipx_key, b.attributes?.ipx_key));

    const counters = entities.filter(e => e.entity_id && e.entity_id.startsWith('sensor.') && e.attributes?.ipx_key && String(e.attributes.ipx_key).startsWith('count'));
    counters.sort((a, b) => this._sortIpxKeys(a.attributes?.ipx_key, b.attributes?.ipx_key));

    const connectionEntity = entities.find(e => e.attributes && e.attributes.ipx_key === 'api_connectivity');
    const isOnline = connectionEntity ? connectionEntity.state === 'on' : true;
    const statusText = connectionEntity ? (isOnline ? "Online" : "Offline") : "Unknown";

    const relayColumns = this.config.relay_columns || 4;
    const inputColumns = this.config.input_columns || 4;
    const analogColumns = this.config.analog_columns || 2;

    const cardTitle = this.config.title || (connectionEntity?.attributes?.friendly_name ? connectionEntity.attributes.friendly_name.replace(" API connectivity", "") : "IPX800 V3 Panel");

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

        ${analogs.length > 0 ? html`
          <div class="section-title">Analog Inputs</div>
          <div class="grid analog-grid">
            ${analogs.map(stateObj => {
              let val = stateObj.state;
              const numVal = parseFloat(val);
              if (!isNaN(numVal)) {
                val = numVal.toFixed(1);
              }

              const unit = stateObj.attributes?.unit_of_measurement || '';
              const name = this._cleanEntityName(stateObj, 'analog');
              const deviceClass = stateObj.attributes?.device_class;
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

        ${relays.length === 0 && inputs.length === 0 && analogs.length === 0 && counters.length === 0 ? html`
          <div style="padding: 20px 0; text-align: center; color: var(--secondary-text-color); font-style: italic;">
            Aucune entité IPX800 trouvée.
          </div>
        ` : ''}
      </ha-card>
    `;
  }

  _sortIpxKeys(keyA, keyB) {
    if (!keyA || !keyB) return 0;
    const numA = parseInt(String(keyA).replace(/^\D+/g, ''), 10) || 0;
    const numB = parseInt(String(keyB).replace(/^\D+/g, ''), 10) || 0;
    return numA - numB;
  }

  _cleanEntityName(stateObj, type) {
    let name = stateObj.attributes?.friendly_name || '';
    if (!name) {
      const parts = (stateObj.entity_id || '').split('.');
      return parts[parts.length - 1];
    }
    name = name.replace(/^My IPX800 V3\s+/i, '');
    name = name.replace(/^IPX800\s+/i, '');
    return name;
  }

  _getAnalogIcon(deviceClass) {
    switch (deviceClass) {
      case 'temperature': return 'mdi:thermometer';
      case 'illuminance': return 'mdi:weather-sunny';
      case 'humidity': return 'mdi:water-percent';
      case 'current': return 'mdi:flash';
      case 'voltage': return 'mdi:sine-wave';
      case 'ph': return 'mdi:ph';
      default: return 'mdi:gauge';
    }
  }

  _fireHaptic(type = "light") {
    try {
      const event = new Event("haptic", { bubbles: true, composed: true });
      event.detail = type;
      this.dispatchEvent(event);
    } catch (e) {
      // Ignoré silencieusement sur les appareils sans support haptique (Nest Hub)
    }
  }

  _toggleSwitch(entityId) {
    this._fireHaptic("light");
    this.hass.callService('switch', 'toggle', { entity_id: entityId });
  }

  _adjustCounter(entityId, offset) {
    this._fireHaptic("medium");
    this.hass.callService('my_ipx800v3', 'adjust_counter_value', {
      entity_id: entityId,
      offset: offset
    });
  }

  setConfig(config) {
    if (!config) {
      throw new Error("Configuration invalide");
    }
    this.config = config;
  }

  getCardSize() {
    return 3;
  }

  static getConfigElement() {
    // Si ha-form n'existe pas (Cast / Nest Hub), ne charge pas l'éditeur visuel
    if (!customElements.get("ha-form")) {
      return document.createElement("div");
    }
    return document.createElement("ipx800v3-card-editor");
  }
}

/**
 * UI Editor pour PC / Mobile
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

    if (!customElements.get("ha-form")) {
      return html`<div>L'éditeur n'est pas disponible sur cet appareil.</div>`;
    }

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
        name: "device_exclude",
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
        .computeLabel=${(schema) => this._computeLabel(schema)}
        @value-changed=${this._onValueChanged}
      ></ha-form>
    `;
  }

  _computeLabel(schema) {
    const lang = this.hass?.language || 'en';
    const baseLang = lang.split('-')[0];
    const dict = editorTranslations[baseLang] || editorTranslations['en'];
    return dict[schema.name] || schema.name;
  }

  _onValueChanged(ev) {
    if (!this._config || !this.hass) {
      return;
    }

    const event = new CustomEvent("config-changed", {
      detail: { config: ev.detail.value },
      bubbles: true,
      composed: true,
    });
    this.dispatchEvent(event);
  }
}

customElements.define('ipx800v3-card', IPX800V3Card);

// Enregistrement sécurisé de l'éditeur uniquement sur PC/Mobile
if (customElements.get("ha-form")) {
  customElements.define("ipx800v3-card-editor", IPX800V3CardEditor);
}

window.customCards = window.customCards || [];
window.customCards.push({
  type: 'ipx800v3-card',
  name: 'IPX800 V3 Card',
  description: 'A dense synthetic card displaying Relays, Digital Inputs, Analogs, and Counters for IPX800 V3 custom integration.',
  preview: true,
  documentationURL: 'https://github.com/amg0/ha_ipx800v3'
});
