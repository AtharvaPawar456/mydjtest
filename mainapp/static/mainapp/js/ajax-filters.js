/**
 * Generic progressive-enhancement helper for GET-based filter/search UIs.
 *
 * Wrap a filter form/links + their results container in one persistent
 * element carrying `data-ajax-filter` and `data-ajax-target="<selector>"`.
 * Clicking a link or submitting a GET form inside that element re-fetches
 * just the target container's markup (the server renders the same partial
 * for the `X-Requested-With: XMLHttpRequest` request) instead of doing a
 * full page navigation. Falls back to a normal browser navigation if the
 * fetch fails, so the feature degrades gracefully without JS or on error.
 */
(function () {
  function swap(container, target, url, pushState) {
    container.setAttribute('aria-busy', 'true');
    fetch(url, { headers: { 'X-Requested-With': 'XMLHttpRequest' } })
      .then(function (response) {
        if (!response.ok) {
          throw new Error('Request failed with status ' + response.status);
        }
        return response.text();
      })
      .then(function (html) {
        target.innerHTML = html;
        if (pushState) {
          history.pushState({ ajaxFilter: true }, '', url);
        }
        target.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
      })
      .catch(function () {
        window.location.href = url;
      })
      .finally(function () {
        container.removeAttribute('aria-busy');
      });
  }

  function initContainer(container) {
    var target = document.querySelector(container.dataset.ajaxTarget);
    if (!target) return;

    container.addEventListener('click', function (event) {
      var link = event.target.closest('a[href]');
      if (!link || !container.contains(link)) return;
      if (link.target === '_blank' || link.hasAttribute('download')) return;
      event.preventDefault();
      swap(container, target, link.getAttribute('href'), true);
    });

    container.addEventListener('submit', function (event) {
      var form = event.target;
      if (!container.contains(form) || form.method.toLowerCase() !== 'get') return;
      event.preventDefault();
      var params = new URLSearchParams(new FormData(form));
      var action = form.getAttribute('action') || window.location.pathname;
      swap(container, target, action + '?' + params.toString(), true);
    });

    window.addEventListener('popstate', function () {
      swap(container, target, window.location.pathname + window.location.search, false);
    });
  }

  document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-ajax-filter]').forEach(initContainer);
  });
})();
