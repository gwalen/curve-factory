from brownie import (
    DepositZapBTC,
    DepositZapUSD,
    Factory,
    # MetaImplementationBTC,
    MetaImplementationUSD,
    MetaUSDBalances, # this should be used, remove reference to MetaImplementationUSD
    OwnerProxy,
    accounts,
)
from brownie.network.gas.strategies import GasNowScalingStrategy

# modify me prior to deployment on mainnet!
# DEPLOYER = accounts.at("0x7EeAC6CDdbd1D0B8aF061742D41877D7F707289a", force=True)
# ADMIN = accounts[0] # local network
ADMIN = accounts.load("gw_test_acc") # rinkeby
DEPLOYER = ADMIN
REQUIRED_CONFIRMATIONS = 1
# gas_price = GasNowScalingStrategy("slow", "fast")


# OWNER_ADMIN = "0x40907540d8a6C65c637785e8f8B742ae6b0b9968"
OWNER_ADMIN = ADMIN
# PARAM_ADMIN = "0x4EEb3bA4f221cA16ed4A0cC7254E2E32DF948c5f"
PARAM_ADMIN = ADMIN
# EMERGENCY_ADMIN = "0x00669DF67E4827FCc0E48A1838a8d5AB79281909"
EMERGENCY_ADMIN = ADMIN
GAUGE_MANAGER = ADMIN

# BASE_3POOL = "0x0B306BF915C4d645ff596e518fAf3F9669b97016"  # test network
BASE_3POOL = "0xAa8684e82B496423559587e39986E0f85D988952"    # rinkeby
# BASE_SBTC = "0x7fC77b5c7614E1533320Ea6DDc2Eb61fa00A9714"

# address of FeeDistributor contract from curve-dao contracts
# FEE_RECEIVER_USD = "0xa464e6dcda8ac41e03616f95f4bc98a13b8922dc"
# FEE_RECEIVER_USD = "0xB7f8BC63BbcaD18155201308C8f3540b07f84F5e" # local network
FEE_RECEIVER_USD = "0xB681Cb29c440Ac3E92169F00Aac93c868CBbe812" # rinkeby
# FEE_RECEIVER_BTC = "0xf9fc73496484290142ee856639f69e04465985cd"

def _tx_params():
    return {
        "from": DEPLOYER,
        "required_confs": REQUIRED_CONFIRMATIONS,
        # "gas_price": GasNowScalingStrategy("standard", "fast"),
        "priority_fee": "3 gwei" # use on Rinkeby (EIP-1559) not tested on local dev
    }


def main(deployer=DEPLOYER):
    # factory = Factory.deploy({"from": deployer})
    factory = Factory.deploy(FEE_RECEIVER_USD, _tx_params()) # had to fix it, missing fee receiver address in constructor params

    # implementation_usd = MetaImplementationUSD.deploy({"from": deployer}) # had to remove gas_price param - Vyper error : ValueError: Expecting value: line 1 column 1 (char 0)
    implementation_usd = MetaUSDBalances.deploy(_tx_params()) # had to remove gas_price param - Vyper error : ValueError: Expecting value: line 1 column 1 (char 0)
    factory.add_base_pool(
        # BASE_3POOL, implementation_usd, FEE_RECEIVER_USD, {"from": deployer, "gas_price": gas_price}
        # had to fix again those constructor params were totally wrong (!?)
        BASE_3POOL, FEE_RECEIVER_USD, 0, [implementation_usd], _tx_params()
    )

    # implementation_btc = MetaImplementationBTC.deploy({"from": deployer, "gas_price": gas_price})
    # factory.add_base_pool(
    #     BASE_SBTC, implementation_btc, FEE_RECEIVER_BTC, {"from": deployer, "gas_price": gas_price}
    # )

    proxy = OwnerProxy.deploy(
        # OWNER_ADMIN, PARAM_ADMIN, EMERGENCY_ADMIN, {"from": deployer} # not enough constructor parameters
        # OWNER_ADMIN, PARAM_ADMIN, EMERGENCY_ADMIN, GAUGE_MANAGER, {"from": deployer}
        OWNER_ADMIN, PARAM_ADMIN, EMERGENCY_ADMIN, GAUGE_MANAGER, _tx_params()
    )

    factory.commit_transfer_ownership(proxy, _tx_params())
    proxy.accept_transfer_ownership(factory, _tx_params())

    DepositZapUSD.deploy(_tx_params())
    # DepositZapBTC.deploy({"from": deployer})
