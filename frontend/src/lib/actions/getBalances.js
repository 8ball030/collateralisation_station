import { fail } from '@sveltejs/kit';
import { deserialize } from '$app/forms';

async function getBalances() {
	const response = await fetch(
		`https://api.etherscan.io/api?module=account&action=addresstokenbalance&address=0x18070D824952Fb5d46F529659BdB497ebB1C5985&apikey=J6V9ADVT3G98PIEWD26WAQ2AYG45P9271Z`,
		{
			method: 'GET'
		}
	);

	console.log(response);
	if (!response.ok) {
		return fail(response.status, { result: 'Failed to get balances' });
	}

	const result = await response.json();

	return result;
}

export default getBalances;
