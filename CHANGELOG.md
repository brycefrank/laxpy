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


