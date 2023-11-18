<script>
	import { getTokens } from '$lib/config/tokens';
	import { MAINNET } from '$lib/config/chains';
	import { CurrencyList } from '$lib/components/CurrencyList';

	export let otherCurrency;
	export let isOpen;
	export let onCurrencySelect;

	let searchQuery;
	function setSearchQuery(input) {
		searchQuery = input;
	}

	const chainId = useChainId();

	const tokensId = chainId && isSupportedChain(chainId) ? chainId : MAINNET;
	const defaultTokens = getTokens(tokensId);
	const filteredTokens = defaultTokens.filter((item) => {
		return (
			item.name.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1 ||
			item.symbol.toLowerCase().indexOf(searchQuery.toLowerCase()) > -1
		);
	});

	$: if (isOpen) {
		setSearchQuery('');
	}

	const handleInput = () => {
		const input = event.target.value;
		setSearchQuery(input);
	};
</script>

<div class="wrapper">
	<div class="row-between"></div>
	<div class="row">
		<input
			class="search-input"
			type="text"
			id="token-search-input"
			autoComplete="off"
			value={searchQuery}
			onChange={handleInput}
		/>
	</div>
	<div class="separator" />
	<div style={{ flex: '1' }}>
		<CurrencyList {otherCurrency} tokens={filteredTokens} {onCurrencySelect} />
	</div>
</div>

<style>
	.wrapper {
		width: 100%;
		flex: 1 1;
		position: relative;
	}
	.search-input {
		background: no-repeat scroll 7px 7px;
		background-size: 20px 20px;
		position: relative;
		display: flex;
		padding: 16px;
		padding-left: 40px;
		height: 20px;
		align-items: center;
		width: 100%;
		white-space: nowrap;
		outline: none;
		border-radius: 12px;
		border-style: solid;
		border: 1px solid grey;
		margin-bottom: 20px;
		font-size: 16px;
		transition: border 100ms;
	}
	.search-input:focus {
		border: 1px solid aqua;
		outline: none;
	}
	.search-input::placeholder {
		color: grey;
		font-size: 16px;
	}
	.separator {
		width: 100%;
		height: 1px;
		background-color: aquamarine;
		margin-bottom: 20px;
	}
	.row,
	.row-between {
		width: 100%;
		display: flex;
		padding: 0;
		align-items: center;
		justify-content: flex-start;
		padding: 6px;
		gap: 10px;
	}
	.row-between {
		justify-content: space-between;
	}
</style>
