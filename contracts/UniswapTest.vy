# @version 0.2.15

from vyper.interfaces import ERC20

UNISWAP_V2_ROUTER: constant(address) = 0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D # testnet / mainnet
# WETH: constant(address) = 0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2              # testnet / mainnet
WETH: constant(address) = 0xc778417E063141139Fce010982780140Aa0cD5Ab              # testnet / mainnet

# fee: public(uint256)

# @external
# def __init__():
#     # empty
#     self.fee = 31337


@external
def swap(
    input_coin: address,
    output_coin: address,
    amountIn: uint256,
    amountOutMin: uint256
):
    ERC20(input_coin).transferFrom(msg.sender, self, amountIn)
    ERC20(input_coin).approve(UNISWAP_V2_ROUTER, amountIn)
    res: Bytes[128] = raw_call(
        UNISWAP_V2_ROUTER,
        concat(
            method_id("swapExactTokensForTokens(uint256,uint256,address[],address,uint256)"),
            convert(amountIn, bytes32),             # amount in
            convert(amountOutMin, bytes32),         # amount out min
            convert(160, bytes32),             # path[] offset (5 * 32, 5 = number of func args before path array)
            convert(msg.sender, bytes32),       # to
            convert(block.timestamp + 1, bytes32), # deadline
            convert(3, bytes32),               # path[] length
            convert(input_coin, bytes32),      # path[0]
            convert(WETH, bytes32),            # path[1]  
            convert(output_coin, bytes32)      # path[2]  
        ),
        max_outsize=128,
    )
    