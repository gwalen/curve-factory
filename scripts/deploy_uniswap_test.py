from brownie import (
    ERC20Mock,
    UniswapTest,
    UniswapTest2,
    accounts,
)
from brownie.network.gas.strategies import GasNowScalingStrategy

# modify me prior to deployment on mainnet!
# DEPLOYER = accounts.at("0x7EeAC6CDdbd1D0B8aF061742D41877D7F707289a", force=True)
ADMIN = accounts.load("gw_test_acc") # rinkeby
DEPLOYER = ADMIN
REQUIRED_CONFIRMATIONS = 1


def _tx_params():
    return {
        "from": DEPLOYER,
        "required_confs": REQUIRED_CONFIRMATIONS,
        "priority_fee": "3 gwei" # use on Rinkeby (EIP-1559) not tested on local dev
    }

def main():
    
    uniswapTest = UniswapTest.deploy(_tx_params())
    # uniswapTest2 = UniswapTest2.deploy(_tx_params())
    gwUSD = ERC20Mock.at('0xB6547B51a2573Ec9118F1218b07567706C2D387d')
    gwUSD.approve(uniswapTest, 20000000000000000000000000, _tx_params())
    dai = ERC20Mock.at('0xF86176aF4687a9E65177913Ebe0A333D79E19fF4')
    dai.approve(uniswapTest, 20000000000000000000000000, _tx_params())
    # uniswapTest.swap(gwUSD, dai, 1*10**18, 0, _tx_params())    
    # uniswapTest2.swap(gwUSD, dai, 1*10**18, {'from': ADMIN, 'priority_fee': '3 gwei', 'gas_limit': 300000})    
    # uniswapTest2.swap(gwUSD, dai, 1*10**18, {'from': ADMIN, 'priority_fee': '3 gwei', 'gas_limit': 300000, 'allow_revert': True})    
    uniswapTest.swap(gwUSD, dai, 1*10**18, 0, {'from': ADMIN, 'priority_fee': '3 gwei', 'gas_limit': 300000, 'allow_revert': True})    
   
