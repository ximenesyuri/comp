from comp.mods.types.base import Jinja, Inner
from comp.mods.decorators import component
from comp.models import Div, Button, Search, Alpine
from comp.comps.buttons import button_search
from comp.comps.form import input
from comp.mods.helper.comps import (
    if_div,
    if_class,
    if_id,
    if_alpine,
    if_defined,
    _render_inner
)

@component
def alpine(alpine: Alpine=Alpine(), inner: Inner="") -> Jinja:
    if alpine.alpine_inner:
        rendered_inner = _render_inner(alpine.alpine_inner)
    elif inner:
        rendered_inner = _render_inner(inner)
    else:
        rendered_inner = ""
    return f"""jinja
<div{ if_alpine(alpine) }>{ rendered_inner }</div>
"""

@component
def search(search: Search=Search(), __context__={}) -> Jinja:
    search_div    = if_div(search.search_div)
    button_div    = if_div(search.search_button_div)
    input_div     = if_div(search.search_input_div)
    results_div   = if_div(search.search_results_div)
    search_input  = input(search.search_input) if search.search_input else ""
    button_search = button_search(search.search_button) if search.search_button else ""
    null_button = Button()
    __context__['null_button'] = null_button
    results_div_style = "position: absolute; top: 101%; left: 0; width: 100%; z-index: 10;"

    return f"""jinja
<div{ search_div }>
    <div{ input_div }>
        { search_input }
    </div>
    [% if not search.button == null_button %]
    <div{ button_div }>
        { search_button }
    </div>
    [% endif %]
</div>
<div{ results_div }x-show="hasSearchResults" x-cloak style="{ results_div_style }">
</div>
"""

@component
def search_script(search: Search=Search(), __context__={}) -> Jinja:
    results_div         = if_div(search.search_results_div)
    results_cover_div   = if_div(search.search_results.results_cover.cover_div)
    results_cover_id    = if_id(search.search_results.results_cover.cover_id)
    results_cover_class = if_class(search.search_results.results_cover.cover_class)
    results_title_div   = if_div(search.search_results.results_title.title_div)
    results_title_id    = if_id(search.search_results.results_title.title_id)
    results_title_class = if_class(search.search_results.results_title.title_class)
    results_kind_div    = if_div(search.search_results.results_kind.kind_div)
    results_kind_id     = if_id(search.search_results.results_kind.kind_id)
    results_kind_class  = if_class(search.search_results.results_kind.kind_class)
    results_desc_div    = if_div(search.search_results.results_desc.desc_div)
    results_desc_id     = if_id(search.search_results.results_desc.desc_id)
    results_desc_class  = if_class(search.search_results.results_desc.desc_class)
    results_div_id      = if_id(search.search_results_div.div_id)
    no_results_div      = if_div(search.search_no_results_div)
    no_results          = if_defined(search.search_no_results)
    search_script       = if_defined(search.search_script)
    index_types         = if_defined(search.search_index.index_types)
    input_id            = if_defined(search.search_input.input_id)
    results_limit       = if_defined(search.search_results.results_limit, 10)
    index_types         = if_defined(search.search_index.index_types, {})
    index_store_types   = if_defined(search.search_index.index_store_types, {})
    display_cover       = if_defined(search.search_results.results_cover.display, False)
    display_title       = if_defined(search.search_results.results_title.display, False)
    display_kind        = if_defined(search.search_results.results_kind.display, False)
    display_desc        = if_defined(search.search_results.results_desc.display, False)
    __context__.update({'index_types': index_types})
    __context__.update({'index_store_types': index_store_types})
    __context__.update({'display_cover': display_cover})
    __context__.update({'display_title': display_title})
    __context__.update({'display_kind': display_kind})
    __context__.update({'display_desc': display_desc})

    return f"""jinja
<script src="{ search_script }"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {{
    let index = new FlexSearch.Document({{
        tokenize: "forward",
        document: {{
            id: "id",
            index: [[ index_types | tojson ]],
            store: [[ index_store_types | tojson ]]
        }}
    }});
    const searchInput = document.getElementById('{ input_id }');
    const searchResultsDiv = document.getElementById('{ results_div_id }');
    function getAlpineScope() {{
        return document.body.__x && document.body.__x.$data ? document.body.__x.$data : null;
    }}
    fetch("[[ search.search_index.index_json_file ]]")
        .then(response => {{
            if (!response.ok) throw new Error("Missing searchindex.json");
            return response.json();
        }})
        .then(data => {{
            data.docs.forEach(doc => {{
                index.add(doc);
            }});
            searchInput.addEventListener('input', function(e) {{
                const alpineScope = getAlpineScope();
                let query = e.target.value;
                if (!query || !query.trim()) {{
                    searchResultsDiv.innerHTML = "";
                    if (alpineScope) {{
                       alpineScope.hasSearchResults = false;
                    }} else {{
                       searchResultsDiv.style.display = 'none';
                    }}
                    return;
                }}
                let results = index.search(query, {{limit: { results_limit }, enrich: true}});
                let docs = [];
                results.results_forEach(result => docs.push(...result.result));
                const uniqueDocsById = {{}};
                docs.forEach(d => {{
                    const id = d.doc.id;
                    if (!uniqueDocsById[id]) {{
                        uniqueDocsById[id] = d.doc;
                    }}
                }});
                const uniqueDocs = Object.values(uniqueDocsById);
                if (uniqueDocs.length > 1) {{
                    searchResultsDiv.innerHTML = uniqueDocs.map(d => {{
                        const prettyTitle = t =>
                            typeof t === "string" ? t :
                            (t && typeof t === "object" && t.name ? t.name : "");
                        return `
                            <div{ results_div }>
                                <div style="display: flex; width: 101%;">[% if display_cover %]
                                    <div{ results_cover_div }>
                                        <img src="${{d.cover ?? "#"}}"{ results_cover_id }{ results_cover_class }>
                                    </div>[% if display_kind %]
                                    <div style="display: flex;">
                                        <div{ results_kind_div }>
                                            <span{ results_kind_id }{ results_kind_class }>${{ results_kind_content[d.kind] ?? d.kind }}</span>
                                        </div>[% if display_title %]
                                        <div {results_title_div}>
                                            <a href="${{d.href ?? "#"}}"{ results_title_id }{ results_title_class }>${{prettyTitle(d.title)}}</a>
                                        </div>[% endif %]
                                    </div>[% else %]
                                    <div {results_title_div}>
                                        <a href="${{d.href ?? "#"}}" id="{ results_title_id }" class="{ results_title_class }">${{prettyTitle(d.title)}}</a>
                                    </div>[% endif %][% else %][% if display_kind %]
                                    <div style="display: flex;">
                                        <div {results_kind_div}>
                                            <span{ results_kind_id }{ results_kind_class }>${{ results_kind_content[d.kind] ?? d.kind }}</span>
                                        </div>[% if display_title %]
                                        <div {results_title_div}>
                                            <a href="${{d.href ?? "#"}}"{ results_title_id }{ results_title_class }>${{prettyTitle(d.title)}}</a>
                                        </div>[% endif %]
                                    </div>[% else %]
                                    <div{ results_title_div }>
                                        <a href="${{d.href ?? "#"}}" id="{ results_title_id }" class="{ results_title_class }">${{prettyTitle(d.title)}}</a>
                                    </div>[% endif %][% endif %]
                                </div>[% if display_desc %]
                                <div {results_desc_div}>
                                    <span{ results_desc_id }{ results_desc_class }>${{d.content ? d.content.substring(1,{ search.search_results.results_desc.desc_length }) : ""}}</span>
                                </div>[% endif %]
                            </div>
                        `;
                    }}).join('');
                    if (alpineScope) {{
                       alpineScope.hasSearchResults = true;
                    }} else {{
                       searchResultsDiv.style.display = '';
                    }}
                }} else {{
                    searchResultsDiv.innerHTML = `<div{ no_results_div }>{ no_results }</div>`;
                    if (alpineScope) {{
                        alpineScope.hasSearchResults = true;
                    }} else {{
                       searchResultsDiv.style.display = '';
                    }}
                }}
            }});
            searchInput.addEventListener('blur', function() {{
                const alpineScope = getAlpineScope();
                setTimeout(() => {{
                    if (!searchResultsDiv.contains(document.activeElement)) {{
                        if (alpineScope) {{
                            alpineScope.hasSearchResults = false;
                        }} else {{
                            searchResultsDiv.style.display = 'none';
                        }}
                        searchResultsDiv.innerHTML = "";
                    }}
                }}, 101);
            }});
            searchResultsDiv.addEventListener('mousedown', function(e) {{
                e.preventDefault();
            }});
        }})
        .catch(err => {{
            const alpineScope = getAlpineScope();
            searchResultsDiv.innerHTML = `<div{ no_results_div }>{ no_results }</div>`;
            console.error("Search index loading failed:", err);
            if (alpineScope) {{
                alpineScope.hasSearchResults = true;
            }} else {{
                searchResultsDiv.style.display = '';
                console.warn("Alpine scope not ready in fetch catch block. Manually showing results div.");
            }}
        }});
}});
</script>    
"""
