# thesis_final


geth --nousb --datadir=$pwd --syncmode 'full' --port 30310 --miner.gasprice 0 --miner.gastarget 470000000000 --http --http.addr 'localhost' --http.port 8545 --http.api admin,eth,miner,net,txpool,personal,web3,shh --mine --shh --allow-insecure-unlock --unlock "0xbB8E9955584486576c609F53Fe9FA4afBa428A73" --password password.txt  

geth --nousb --datadir=$pwd --syncmode 'full' --port 30311 --miner.gasprice 0 --miner.gastarget 470000000000 --http --http.addr 'localhost' --http.port 8545 --http.api admin,eth,miner,net,txpool,personal,web3,shh --mine --shh --allow-insecure-unlock --unlock "0x4527c57D86B48e6fDD9BA3DC95559703a74693a1" --password password.txt  

geth --nousb --datadir=$pwd --syncmode 'full' --port 30312 --miner.gasprice 0 --miner.gastarget 470000000000 --http --http.addr 'localhost' --http.port 8545 --http.api admin,eth,miner,net,txpool,personal,web3,shh --mine --shh --allow-insecure-unlock --unlock "0xbA09cA4257A899B33549fd56A0d833f2457c251B" --password password.txt 





