import {
	readContract as readContractWagmi,
	getNetwork,
	getContract as getContractWagmi,
	getAccount,
	writeContract as writeContractWagmi
} from '@wagmi/core';
import { createPublicClient, http } from 'viem';
import { mainnet, polygon } from 'viem/chains';

/**
 * returns the web3 details
 */
export const getWeb3Details = () => {
	const network = getNetwork();
	const chainId = network.chain?.id || 100;
	const account = getAccount();

	return { account, chainId };
};

/**
 * returns contract interface
 */
export const getContract = (abi, contractAddress) => {
	const contract = getContractWagmi({
		address: contractAddress,
		abi
	});

	return contract;
};

export const readContract = async (abi, address, method, args = []) => {
	const data = await readContractWagmi({
		address,
		abi,
		functionName: method,
		args
	});
	return data;
};

export const writeContract = async (abi, address, method, args = []) => {
	const { hash } = await writeContractWagmi({
		address,
		abi,
		functionName: method,
		args
	});
	return hash;
};

export const publicClient = createPublicClient({
	chain: polygon,
	transport: http()
});
