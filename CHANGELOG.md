## 0.1.9
- Hotfix for empty cell problem, fixes #6

## 0.1.8
- Fixing small bug in `query` that errored on an empty query.

## 0.1.6

- Adding optional conda environment
- Adding Windows testing on Travis
- Reduced the structure of `file.init_lax` check for `lasindex` installation.

## 0.1.2a
- Added warning for empty mappings.

## 0.1.2

- Fixed issue with missing dependencies on pip install

## 0.1

Pre-release version.

### `IndexedLas`

- Removed scale argument from `.query_polygon`, it is now required to scale  (because to query a polygon requires points to be georeferneced, i.e. scaled).


