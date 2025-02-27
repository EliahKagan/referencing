=========
Changelog
=========

v0.30.2
-------

* Minor docs improvement.

v0.30.1
-------

* Ensure that an ``sdist`` contains the test suite JSON files.

v0.30.0
-------

* Declare support for Python 3.12.

v0.29.3
-------

* Documentation fix.

v0.29.2
-------

* Improve the hashability of exceptions when they contain hashable data.


v0.29.1
-------

* Minor docs improvement.

v0.29.0
-------

* Add ``referencing.retrieval.to_cached_resource``, a simple caching decorator useful when writing a retrieval function turning JSON text into resources without repeatedly hitting the network, filesystem, etc.

v0.28.6
-------

* No user-facing changes.

v0.28.5
-------

* Fix a type annotation and fill in some missing test coverage.

v0.28.4
-------

* Fix a type annotation.

v0.28.3
-------

* No user-facing changes.

v0.28.2
-------

* Added some additional packaging trove classifiers.

v0.28.1
-------

* More minor documentation improvements

v0.28.0
-------

* Minor documentation improvement

v0.27.4
-------

* Minor simplification to the docs structure.

v0.27.3
-------

* Also strip fragments when using ``__getitem__`` on URIs with empty fragments.

v0.27.2
-------

* Another fix for looking up anchors from non-canonical URIs, now when they're inside a subresource which has a relative ``$id``.

v0.27.1
-------

* Improve a small number of docstrings.


v0.27.0
-------

* Support looking up anchors from non-canonical URIs.
  In other words, if you add a resource at the URI ``http://example.com``, then looking up the anchor ``http://example.com#foo`` now works even if the resource has some internal ``$id`` saying its canonical URI is ``http://somethingelse.example.com``.

v0.26.4
-------

* Further API documentation.


v0.26.3
-------

* Add some documentation on ``referencing`` public and non-public API.


v0.26.2
-------

* Also suggest a proper JSON Pointer for users who accidentally use ``#/`` and intend to refer to the entire resource.

v0.26.1
-------

* No changes.

v0.26.0
-------

* Attempt to suggest a correction if someone uses '#foo/bar', which is neither a valid plain name anchor (as it contains a slash) nor a valid JSON pointer (as it doesn't start with a slash)

v0.25.3
-------

* Normalize the ID of JSON Schema resources with empty fragments (by removing the fragment).
  Having a schema with an ID with empty fragment is discouraged, and newer versions of the spec may flat-out make it an error, but older meta-schemas indeed used IDs with empty fragments, so some extra normalization was needed and useful here even beyond what was previously done.
  TBD on whether this is exactly right if/when another referencing spec defines differing behavior.

v0.25.2
-------

* Minor tweaks to the package keywords and description.

v0.25.1
-------

* Minor internal tweaks to the docs configuration.

v0.25.0
-------

* Bump the minimum version of ``rpds.py`` used, enabling registries to be used from multiple threads.

v0.24.4
-------

* Fix handling of IDs with empty fragments (which are equivalent to URIs with no fragment)

v0.24.3
-------

* Further intro documentation

v0.24.2
-------

* Fix handling of ``additionalProperties`` with boolean value on Draft 4 (where the boolean isn't a schema, it's a special allowed value)

v0.24.1
-------

* Add a bit of intro documentation

v0.24.0
-------

* ``pyrsistent`` was replaced with ``rpds.py`` (Python bindings to the Rust rpds crate), which seems to be quite a bit faster.
  No user-facing changes really should be expected here.
