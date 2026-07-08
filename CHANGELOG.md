# Changelog

## [0.4.22](https://github.com/amg0/ha_ipx800v3/compare/v0.4.21...v0.4.22) (2026-07-08)


### Features

* improved Lovelace card with responsive design ([56938e3](https://github.com/amg0/ha_ipx800v3/commit/56938e336f8c93cfffc997b0a1b2c21e4566bf2f))


### Bug Fixes

* api connectivity sensor needs the ipx_key attribute ([6221606](https://github.com/amg0/ha_ipx800v3/commit/6221606b5144c3ea080623ef76c5c6899675ad35))

## [0.4.21](https://github.com/amg0/ha_ipx800v3/compare/v0.4.20...v0.4.21) (2026-07-03)

- change log ([2b5c944](https://github.com/amg0/ha_ipx800v3/commit/2b5c9449b55c7d14ba672c7eb9c82d57daac38d8))
- extend latency to 200ms in case of webhook to let IPX800 NIC cool down ([ff0e3cd](https://github.com/amg0/ha_ipx800v3/commit/ff0e3cd878fa082aa209bf3f9bc15753e17b08fe))

## [0.4.20](https://github.com/amg0/ha_ipx800v3/compare/v0.4.19...v0.4.20) (2026-07-03)

- remove blocking call for displaying version ([107d05e](https://github.com/amg0/ha_ipx800v3/commit/107d05e94545ec8236eb22b0af9237142ec091e9))

## [0.4.19](https://github.com/amg0/ha_ipx800v3/compare/v0.4.18...v0.4.19) (2026-06-30)

- remove blocking call to read manifest file ([6e135b0](https://github.com/amg0/ha_ipx800v3/commit/6e135b001fdaf2e610c84b1c3733577dc1058d4d))

## [0.4.18](https://github.com/amg0/ha_ipx800v3/compare/v0.4.17...v0.4.18) (2026-06-29)

- add trace on integration startup ([a13329f](https://github.com/amg0/ha_ipx800v3/commit/a13329f1779f8dd936ea75f0a8389c34d5d670f4))

## [0.4.17](https://github.com/amg0/ha_ipx800v3/compare/v0.1.0...v0.4.17) (2026-06-29)

- add a debug statemet to display received data ([7b71793](https://github.com/amg0/ha_ipx800v3/commit/7b71793e69d59fe8405ca64a3c6f542563f0d8cb))
- add a latency in the webhook handler ([deef68f](https://github.com/amg0/ha_ipx800v3/commit/deef68f4c58723649beff1c69038baf3723b33e4))
- Add debug to track intermittent problem ([805c869](https://github.com/amg0/ha_ipx800v3/commit/805c86981dc65709809d2ad4adee5680fbfc1e39))
- introduce a small latency in the webhook treatment ([aebb709](https://github.com/amg0/ha_ipx800v3/commit/aebb709813c98a50e78a78d5fe539ef541a79db8))
- restrict the filtering of invalid data with an and instead of or for the conditions ([e70b3df](https://github.com/amg0/ha_ipx800v3/commit/e70b3df1566b2636cfab0dbf95b822b2be37ea3c))
- try to ignore invalid data when all values are zero and ddnsstatus is pending ([e90a553](https://github.com/amg0/ha_ipx800v3/commit/e90a553b1dde3dda0e9b2a3f235cffc1f020e583))
- version 0.4.15 ([578c3c5](https://github.com/amg0/ha_ipx800v3/commit/578c3c502e1906c1fac5c2f4acf4f393b141d627))
