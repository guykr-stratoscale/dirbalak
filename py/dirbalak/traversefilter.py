class TraverseFilter:
    def __init__(self, traverse, dirbalakBuildRootFSArcs=True, solventRootFSArcs=True):
        self._traverse = traverse
        self._dirbalakBuildRootFSArcs = dirbalakBuildRootFSArcs
        self._solventRootFSArcs = solventRootFSArcs

    def dependencies(self):
        return [d for d in self._traverse.dependencies() if not self._skip(d)]

    def _skip(self, dep):
        if not self._dirbalakBuildRootFSArcs:
            if dep.type == "dirbalak_build_rootfs":
                return True
        if not self._solventRootFSArcs:
            if dep.type == "solvent" and self._gitURLIsARootFS(dep.gitURL) and \
                    not self._gitURLIsARootFS(dep.requiringURL):
                return True
        return False

    def _gitURLIsARootFS(self, gitURL):
        return '/rootfs-' in gitURL
