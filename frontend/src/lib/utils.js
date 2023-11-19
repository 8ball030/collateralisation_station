import {
	readContract as readContractWagmi,
	getNetwork,
	getContract as getContractWagmi,
	getAccount,
	writeContract as writeContractWagmi
} from '@wagmi/core';
import { createPublicClient, http } from 'viem';
import { mainnet } from 'viem/chains';

// const MAINNET_ADDRESSES: { [key: string]: `0x${string}` } = {
//   agentRegistry: "0x2F1f7D38e4772884b88f3eCd8B6b9faCdC319112",
//   componentRegistry: "0x15bd56669F57192a97dF41A2aa8f4403e9491776",
//   registriesManager: "0x9eC9156dEF5C613B2a7D4c46C383F9B58DfcD6fE",
//   serviceManagerToken: "0x2EA682121f815FBcF86EA3F3CaFdd5d67F2dB143",
//   serviceRegistry: "0x48b6af7B12C71f09e2fC8aF4855De4Ff54e775cA",
//   serviceRegistryTokenUtility: "0x3Fb926116D454b95c669B6Bf2E7c3bad8d19affA",
//   operatorWhitelist: "0x42042799B0DE38AdD2a70dc996f69f98E1a85260",
//  };

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
	chain: mainnet,
	transport: http()
});
