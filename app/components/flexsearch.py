from app.mods.types.base import Jinja
from app.mods.decorators.base import component
from app.models import Div, Button, FlexSearch
from app.components.inputs  import input_search
from app.components.buttons import button_search
from app.helper import if_div, if_class, if_id

@component
def flexsearch(flexsearch: FlexSearch=FlexSearch(), __depends_on__=[button_search, input_search], __context__={}) -> Jinja:
    search_div          = if_div(flexsearch.div)
    button_div          = if_div(flexsearch.button_div)
    input_div           = if_div(flexsearch.input_div)
    results_div         = if_div(flexsearch.results_div)
    results_cover_div   = if_div(flexsearch.results.cover.cover_div)
    results_cover_id    = if_id(flexsearch.results.cover.cover_id)
    results_cover_class = if_class(flexsearch.results.cover.cover_class)
    results_title_div   = if_div(flexsearch.results.title.title_div)
    results_title_id    = if_id(flexsearch.results.title.title_id)
    results_title_class = if_class(flexsearch.results.title.title_class)
    results_kind_div    = if_div(flexsearch.results.kind.kind_div)
    results_kind_id     = if_id(flexsearch.results.kind.kind_id)
    results_kind_class  = if_class(flexsearch.results.kind.kind_class)
    results_desc_div    = if_div(flexsearch.results.desc.desc_div)
    results_desc_id     = if_id(flexsearch.results.desc.desc_id)
    results_desc_class  = if_class(flexsearch.results.desc.desc_class)
    no_results_div      = if_div(flexsearch.no_results_div)
    null_button         = Button()
    __context__['null_button'] = null_button
    results_div_style = "position: absolute; top: 101%; left: 0; width: 100%; z-index: 10;"

    return f"""jinja
<div { search_div }>
    <div { input_div } >
        { input_search(flexsearch.input) }
    </div>
    [% if not flexsearch.button == null_button %]
    <div { button_div }>
        { button_search(flexsearch.button) }
    </div>
    [% endif %]
</div>
<div { results_div } x-show="hasSearchResults" x-cloak
    style="{ results_div_style }"
>
</div>
<script src="{ flexsearch.script_url }"></script>
<script>
document.addEventListener("DOMContentLoaded", function() {{
    let index = new FlexSearch.Document({{
        tokenize: "forward",
        document: {{
            id: "id",
            index: [[ flexsearch.index.index_types | tojson ]],
            store: [[ flexsearch.index.index_store_types | tojson ]]
        }}
    }});
    const searchInput = document.getElementById('{ flexsearch.input.input_id }');
    const searchResultsDiv = document.getElementById('{ flexsearch.results_div.div_id }');
    function getAlpineScope() {{
        return document.body.__x && document.body.__x.$data ? document.body.__x.$data : null;
    }}
    fetch("[[ flexsearch.index.index_json_file ]]")
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
                let results = index.search(query, {{limit: { flexsearch.results.limit }, enrich: true}});
                let docs = [];
                results.forEach(result => docs.push(...result.result));
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
                            <div {results_div}>
                                <div style="display: flex; width: 101%;">
                                    [% if flexsearch.results.cover.display %]
                                        <div {results_cover_div}>
                                            <img src="${{d.cover ?? "#"}}"{results_cover_id}{results_cover_class}>
                                        </div>
                                        [% if flexsearch.results.kind.display %]
                                        <div style="display: flex;">
                                            <div {results_kind_div}>
                                                <span {results_kind_id}{results_kind_class}>${{ results_kind_content[d.kind] ?? d.kind }}</span>
                                            </div>
                                            [% if flexsearch.results.title.display %]
                                            <div {results_title_div}>
                                                <a href="${{d.href ?? "#"}}"{results_title_id}{results_title_class}>${{prettyTitle(d.title)}}</a>
                                            </div>
                                            [% endif %]
                                        </div>
                                        [% else %]
                                        <div {results_title_div}>
                                            <a href="${{d.href ?? "#"}}" id="{results_title_id}" class="{results_title_class}">${{prettyTitle(d.title)}}</a>
                                        </div>
                                        [% endif %]
                                    [% else %]
                                        [% if flexsearch.results.kind.display %]
                                        <div style="display: flex;">
                                            <div {results_kind_div}>
                                                <span {results_kind_id}{results_kind_class}>${{ results_kind_content[d.kind] ?? d.kind }}</span>
                                            </div>
                                            [% if flexsearch.results.title.display %]
                                            <div {results_title_div}>
                                                <a href="${{d.href ?? "#"}}"{results_title_id}{results_title_class}>${{prettyTitle(d.title)}}</a>
                                            </div>
                                            [% endif %]
                                        </div>
                                        [% else %]
                                        <div {results_title_div}>
                                            <a href="${{d.href ?? "#"}}" id="{results_title_id}" class="{results_title_class}">${{prettyTitle(d.title)}}</a>
                                        </div>
                                        [% endif %]
                                    [% endif %]
                                </div>
                                [% if flexsearch.results.desc.display %]
                                <div {results_desc_div}>
                                    <span {results_desc_id}{results_desc_class}>${{d.content ? d.content.substring(1,{ flexsearch.results.desc.desc_length }) : ""}}</span>
                                </div>
                                [% endif %]
                            </div>
                        `;
                    }}).join('');
                    if (alpineScope) {{
                       alpineScope.hasSearchResults = true;
                    }} else {{
                       searchResultsDiv.style.display = '';
                    }}
                }} else {{
                    searchResultsDiv.innerHTML = `<div {no_results_div}>{ flexsearch.no_results }</div>`;
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
            searchResultsDiv.innerHTML = `<div {no_results_div}>{ flexsearch.no_results }</div>`;
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

