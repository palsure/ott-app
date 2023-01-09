#!/bin/bash
export DATABASE_URL="postgresql://postgres@localhost:5432/ottapp"
export EXCITED="true"
export AUTH0_DOMAIN='sure-ott.us.auth0.com'
export ALGORITHMS=['RS256']
export API_AUDIENCE='sure-ott'
export OTT_MANAGER_JWT='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVuQjByMUR3LUYwcHU2QjNpeWxxRiJ9.eyJpc3MiOiJodHRwczovL3N1cmUtb3R0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2JhZDFkM2NkOGIyMmQyZDdjNWJhZWEiLCJhdWQiOiJzdXJlLW90dCIsImlhdCI6MTY3MzE5Mzg4MSwiZXhwIjoxNjczMjgwMjgxLCJhenAiOiI3cnQ1elZqVDZoNTFmMEtLdzB2dUFJN0tnSnEzY0Q1eSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOm90dCIsInBhdGNoOm90dCIsInBvc3Q6b3R0IiwicmVhZDpvdHQiXX0.vi5isoLAcgBUb3EzbbF9hyNlsV2cRoEhnvGt6Ycu27wmYLbhhBXne6LWxqMhyLifuK0x9cxze0qoHrnDgqWXk77M9FPcvrUeT9AXQgT5zDoEH1n6vmz-7xOArRtLlLmo-gPDMZWDZWYCDRuOmnQqQINBMngQmVmnuKoXdTXBepgVFAYhL90caqgrD8xGhED61aSoOdRG6dtZBIgmxK_wHL3IBZcJ3DJBQf-3x3FEm9eFpgx-JcWrsMW6gJqI70G39_BtUkt4a6Tq2znHDiWFT5iNVVlcHxzCFUn67YsiYG370gV1_WXX84ZEgGRpvlAi9fbnP-d4r1Whv_iJZOSpew'
export OTT_USER_JWT='Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImVuQjByMUR3LUYwcHU2QjNpeWxxRiJ9.eyJpc3MiOiJodHRwczovL3N1cmUtb3R0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2M2JhZDRjMjQxMDg4MjJhMWVmMzg3YmQiLCJhdWQiOiJzdXJlLW90dCIsImlhdCI6MTY3MzE5NDAyNCwiZXhwIjoxNjczMjgwNDI0LCJhenAiOiI3cnQ1elZqVDZoNTFmMEtLdzB2dUFJN0tnSnEzY0Q1eSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDpvdHQiXX0.X0TjYAdcfocO2-d7I-JGiulV4iiZ_pK3h2sY-BZDot28DA1GONUSgozeoyRqhqiO7UYqOOws2YtHGJjz0WZpwUYnAXxawSlqkgm47g6plsjQJwzhqmsQ8ShHmFyE4VBI9i7D0KeQ-0lrKbgveArfkwhvOLkxldUGU3sI9PigFsACT1Pb4fy9FuMCTzhlb9GBgCaan4ueKZ09pC-nnSf561dWh10S3q72rQBmshHdpQO8w8ACjE-7rf2MWq-bjdszWC7WUhmxSFX-ipdnaiYj5N6o0F1XHjNVbiMjIlL9ZUeLYZkIq1CrCrsod7AIzsntvCuyfL3Q3Rf5x6DIAsMnIg'
echo "setup.sh script executed successfully!"