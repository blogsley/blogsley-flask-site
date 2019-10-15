/*
const element = document.getElementById('applet');
const shadowRoot = element.attachShadow({mode: 'open'});
const template = document.querySelector('#appletTemplate');
shadowRoot.appendChild(template.content.cloneNode(true));
*/
/*
shadowRoot.innerHTML = `
<link href="/static/css/blocksley.css" rel="stylesheet" type="text/css">
<div id="q-app"><slot></slot></div>
<script src="/static/js/blocksley.js"></script>
`;
*/
(function() {
  /*
  const template = document.createElement('template');

  template.innerHTML = `
    <link href="/static/css/blocksley.css" rel="stylesheet" type="text/css">
    <script src="/static/js/blocksley.js"></script>
    <slot></slot>
  `;
  */
  const template = document.querySelector('#appletTemplate');
  class QuasarApp extends HTMLElement {
    constructor() {
      super();

      this.attachShadow({ mode: 'open' });
      this.shadowRoot.appendChild(template.content.cloneNode(true));
    }
  }

  window.customElements.define('quasar-app', QuasarApp);
})();