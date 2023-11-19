<script>
	const inputRegex = RegExp(`^\\d*(?:\\\\[.])?\\d*$`);

	export let value;
	export let onUserInput;
	export let placeholder;
	export let prependSymbol;

	function handleOnChange(event) {
		if (prependSymbol) {
			const value = event.target.value;

			const formattedValue = value.toString().includes(prependSymbol)
				? value.toString().slice(1, value.toString().length + 1)
				: value;

			console.log(enforcer);
			enforcer(formattedValue.replace(/,/g, '.'));
		} else {
			enforcer(event.target.value.replace(/,/g, '.'));
		}
	}
</script>

<input
	class="token-input"
	value={prependSymbol && value ? prependSymbol + value : value}
	onChange={handleOnChange}
	inputMode="decimal"
	autoComplete="off"
	autoCorrect="off"
	type="text"
	pattern="^[0-9]*[.,]?[0-9]*$"
	minLength={1}
	maxLength={79}
	spellCheck="false"
/>

<style>
	.token-input {
		width: 0px;
		position: relative;
		font-weight: 500;
		outline: none;
		border: none;
		flex: 1 1 auto;
		background-color: transparent;
		font-size: 28px;
		overflow: hidden;
		text-overflow: ellipsis;
		text-align: left;
	}
</style>
