import tempfile
import subprocess
import logging


class Graph:
    def __init__(self, graphAttributes):
        self._graphAttributes = graphAttributes
        self._arcs = {}
        self._attributes = {}

    def saveDot(self, filename):
        with open(filename, "w") as f:
            f.write(self._dotContents())

    def saveSvg(self, filename):
        assert filename.endswith(".svg")
        dot = tempfile.NamedTemporaryFile(suffix=".dot")
        dot.write(self._dotContents())
        dot.flush()
        try:
            _run(["dot", dot.name, "-Tsvg", "-o", filename])
        except:
            with open("/tmp/notworky.dot", "w") as f:
                f.write(self._dotContents())
            logging.info("Saved last .dot file in /tmp/notworky.dot")
            raise

    def svgAndMap(self):
        svg = tempfile.NamedTemporaryFile(suffix=".svg")
        map = tempfile.NamedTemporaryFile(suffix=".map")
        dot = tempfile.NamedTemporaryFile(suffix=".dot")
        dot.write(self._dotContents())
        dot.flush()
        try:
            _run(["dot", dot.name, "-Tcmap", "-o", map.name, "-Tsvg", "-o", svg.name])
        except:
            with open("/tmp/notworky.dot", "w") as f:
                f.write(self._dotContents())
            logging.info("Saved last .dot file in /tmp/notworky.dot")
            raise
        with open(map.name) as f:
            mapContents = f.read()
        with open(svg.name, "rb") as f:
            svgContents = f.read()
        return svgContents, mapContents

    def addArc(self, source, dest, **attributes):
        self._arcs.setdefault(source, dict())[dest] = attributes

    def setNodeAttributes(self, node, **attributes):
        self._attributes[node] = attributes

    def _attributesToString(self, attributes, join=', '):
        withQuotations = dict(attributes)
        TO_QUOTE = ['label', 'color', 'URL', 'fillcolor']
        for toQuote in TO_QUOTE + [k for k in withQuotations if k.startswith("text_")]:
            if toQuote in withQuotations:
                withQuotations[toQuote] = '"' + withQuotations[toQuote] + '"'
        if 'cluster' in withQuotations:
            del withQuotations['cluster']
        return join.join(["%s=%s" % (k, v) for k, v in withQuotations.iteritems()])

    def _dotContents(self):
        result = ["digraph G {"]
        result.append(self._attributesToString(self._graphAttributes, join='\n'))
        clusters = set()
        for node, attributes in self._attributes.iteritems():
            cluster = attributes.get('cluster', None)
            if cluster is None:
                result.append('"%s" [ %s ];' % (node, self._attributesToString(attributes)))
            else:
                clusters.add(cluster)
        for cluster in clusters:
            result.append("subgraph cluster_%s {" % cluster)
            result.append('label = "%s"' % cluster)
            for node, attributes in self._attributes.iteritems():
                if attributes.get('cluster', None) == cluster:
                    result.append('"%s" [ %s ];' % (node, self._attributesToString(attributes)))
            for source, arcs in self._arcs.iteritems():
                for dest, attributes in arcs.iteritems():
                    sourceSubgraph = self._attributes[source].get('cluster', None)
                    destSubgraph = self._attributes[dest].get('cluster', None)
                    if sourceSubgraph == cluster and destSubgraph == cluster:
                        result.append('"%s" -> "%s" [ %s ];' % (
                            source, dest, self._attributesToString(attributes)))
            result.append("}")
        for source, arcs in self._arcs.iteritems():
            for dest, attributes in arcs.iteritems():
                sourceSubgraph = self._attributes[source].get('cluster', None)
                destSubgraph = self._attributes[dest].get('cluster', None)
                if sourceSubgraph is not None and sourceSubgraph != destSubgraph:
                    result.append('"%s" -> "%s" [ %s ];' % (
                        source, dest, self._attributesToString(attributes)))
        result.append("}")
        return "\n".join(result)

    def _digraphSources(self):
        withoutIncomingArcs = set(self._arcs.keys()) | set(self._attributes.keys())
        for froms, dests in self._arcs.iteritems():
            for d in dests:
                withoutIncomingArcs.discard(d)
        return withoutIncomingArcs

    def renderAsTreeText(self, indentation="    "):
        result = []
        for source in self._digraphSources():
            result += self._treeIterate(source, 0)
        return "\n".join(indentation * l[1] + l[0] for l in result)

    def _treeIterate(self, node, depth):
        attributes = self._attributes.get(node, dict())
        label = attributes.get('label', node).replace("\n", "\t")
        textAttributes = "  ".join([attributes[text] for text in attributes if text.startswith('text_')])
        result = [(label + "  " + textAttributes, depth)]
        for dest, attributes in self._arcs.get(node, dict()).iteritems():
            if 'label' in attributes:
                result.append(('VV ' + attributes['label'].replace("\\n", "  "), depth + 1))
            if depth > 7:
                result.append(('RECURSION TOO DEEP', depth + 1))
                continue
            result += self._treeIterate(dest, depth + 1)
        return result


def _run(command, cwd=None):
    try:
        return subprocess.check_output(
            command, cwd=cwd, stderr=subprocess.STDOUT,
            stdin=open("/dev/null"), close_fds=True)
    except subprocess.CalledProcessError as e:
        logging.error("Failed command '%s' output:\n%s" % (command, e.output))
        raise


if __name__ == "__main__":
    g = Graph()
    g.addArc("here", "there")
    g.addArc("there", "back again")
    g.setNodeAttributes("back again", label="first line\nsecond line")
    g.saveSvg("/tmp/t.svg")
