import { getNetwork, getAccount } from '@wagmi/core';

/**
 * returns the web3 details
 */
export const getWeb3Details = () => {
	const network = getNetwork();
	const chainId = network.chain?.id || 100;
	const account = getAccount();

	return { account, chainId };
};
