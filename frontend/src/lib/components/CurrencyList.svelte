<script>
	export let tokens;
	export let handleCurrencySelect;
</script>

<div class="token-selector-tokens">
	{#each tokens as token (token.address)}
		<div class="token-row" on:click={() => handleCurrencySelect(token.symbol)}>
			<div class="token-info">
				<img class="token-logo" src={token.imageUrl} alt={token.name} />
				<div class="box">
					<div class="token-symbol">
						<div class="token-text">{token.symbol}</div>
					</div>
					<div class="token-name">
						<span class="text-accent">{token.name}</span>
					</div>
				</div>
			</div>
		</div>
	{/each}
</div>

<style>
	.token-row {
		border: none;
		margin: 0.5rem;
		padding: 0.5rem;
		border-radius: 12px;
	}
	.token-row:hover {
		cursor: pointer;
		/* background-color: var(--surface2); */
	}
	.token-info {
		display: flex;
		flex-direction: row;
		justify-content: left;
		align-items: center;
	}
	.token-logo {
		width: 2.5rem;
		height: 2.5rem;
		margin-right: 0.8rem;
	}
	.token-symbol,
	.token-name {
		margin-left: 0.8rem;
		display: flex;
		flex-direction: column;
	}
	.token-symbol {
		font-weight: 600;
	}
	.token-name {
		color: #292929;
	}
</style>
