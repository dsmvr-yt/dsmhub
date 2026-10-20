"""Shared helper: wrap an HTML document into an SVG that jsDelivr serves in a script-running form."""
import base64

VIEWPORT = ('<foreignObject x="0" y="0" width="0" height="0"><meta xmlns="http://www.w3.org/1999/xhtml" '
            'name="viewport" content="width=device-width, initial-scale=1"/></foreignObject>')

def wrap(html: str, sandbox: str, title: str = "DSMHub") -> str:
    b64 = base64.b64encode(html.encode("utf-8")).decode()
    title = title.replace("&", "&amp;").replace("<", "&lt;")
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="100%" height="100%"><title>' + title + '</title>'
        + VIEWPORT + '<foreignObject id="f" x="0" y="0" width="100%" height="100%"/>'
        '<script><![CDATA[(function(){var b="' + b64 + '";'
        'var h=new TextDecoder().decode(Uint8Array.from(atob(b),function(c){return c.charCodeAt(0)}));'
        'var i=document.createElementNS("http://www.w3.org/1999/xhtml","iframe");'
        'i.setAttribute("style","border:0;width:100%;height:100%");i.setAttribute("allow","fullscreen");'
        'i.setAttribute("sandbox","' + sandbox + '");i.setAttribute("srcdoc",h);'
        'document.getElementById("f").appendChild(i)})();]]></script></svg>\n'
    )
