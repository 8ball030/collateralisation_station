import { GNOSIS } from '$lib/config/chains';

export const TOKENS = {
	[GNOSIS]: [
		{
			name: 'Dai Stablecoin',
			symbol: 'DAI',
			decimals: 18,
			address: '0x44fA8E6f47987339850636F88629646662444217',
			isStable: true,
			imageUrl: '/dai.png'
		},
		{
			name: 'OLAS',
			symbol: 'OLAS',
			decimals: 18,
			address: '0x79C872Ed3Acb3fc5770dd8a0cD9Cd5dB3B3Ac985',
			isStable: true,
			imageUrl: '/olas.png'
		}
	]
};

const CHAIN_IDS = [GNOSIS];

export const TOKENS_MAP = {};
export const TOKENS_BY_SYMBOL_MAP = {};

for (let j = 0; j < CHAIN_IDS.length; j++) {
	const chainId = CHAIN_IDS[j];
	TOKENS_MAP[chainId] = {};
	TOKENS_BY_SYMBOL_MAP[chainId] = {};
	let tokens = TOKENS[chainId];

	for (let i = 0; i < tokens.length; i++) {
		const token = tokens[i];
		TOKENS_MAP[chainId][token.address] = token;
		TOKENS_BY_SYMBOL_MAP[chainId][token.symbol] = token;
	}
}

export function getTokens(chainId) {
	return TOKENS[chainId];
}

export function isValidToken(chainId, address) {
	if (!TOKENS_MAP[chainId]) {
		throw new Error(`Incorrect chainId ${chainId}`);
	}
	return address in TOKENS_MAP[chainId];
}

export function getToken(chainId, address) {
	if (!TOKENS_MAP[chainId]) {
		throw new Error(`Incorrect chainId ${chainId}`);
	}
	if (!TOKENS_MAP[chainId][address]) {
		throw new Error(`Incorrect address "${address}" for chainId ${chainId}`);
	}
	return TOKENS_MAP[chainId][address];
}

export function getTokenBySymbol(chainId, symbol) {
	const token = TOKENS_BY_SYMBOL_MAP[chainId][symbol];
	if (!token) {
		console.log(`Incorrect symbol "${symbol}" for chainId ${chainId}`);
	}
	return token;
}

export const getLogo = (currency, chainId) => {
	if (currency && !!chainId) {
		const token = getTokenBySymbol(chainId, currency);
		if (!token) return null;
		return token.imageUrl;
	}
	return null;
};
