import { useEffect, useState } from 'react'

type Player = 'X' | 'O'
type Cell = 'X' | 'O' | ' '
type Board = Cell[][]

export default function App() {
	const [board, setBoard] = useState<Board>(Array.from({ length: 6 }, () => Array.from({ length: 6 }, () => ' ')))
	const [winningPlayer, setWinningPlayer] = useState<'X' | 'O' | null>(null)
	const [currentPlayer, setCurrentPlayer] = useState<'X' | 'O'>('X')
	const [openLocations, setOpenLocations] = useState<number[]>([0, 1, 2, 3, 4, 5])
	const [currentSuggestion, setCurrentSuggestion] = useState<{
		column_scores: Record<string, number>
		top_suggestion: {
			column: number
			score: number
		}
	} | null>(null)

	async function makeMove(column: number) {
		const response = await fetch('/api/move', {
			method: 'POST',
			body: JSON.stringify({
				board: board,
				current_player: currentPlayer,
				column,
			}),
			headers: {
				'Content-Type': 'application/json',
			},
		})
		const data = (await response.json()) as {
			current_board: Board
			open_locations: number[]
			board_state: {
				is_game_won: boolean
				winner: Player | null
			}
		}
		setOpenLocations(data.open_locations)
		setCurrentPlayer((curr) => (curr == 'X' ? 'O' : 'X'))
		setBoard(data.current_board)
		if (data.board_state.is_game_won) {
			setWinningPlayer(data.board_state.winner)
		}
	}

	useEffect(() => {
		suggestMove()
	}, [board])

	async function suggestMove() {
		const response = await fetch('/api/suggest', {
			method: 'POST',
			body: JSON.stringify({
				board: board,
				current_player: currentPlayer,
				max_depth: 4,
			}),
			headers: {
				'Content-Type': 'application/json',
			},
		})
		const data = await response.json()
		setCurrentSuggestion(data)
	}

	return (
		<main className='p-5 mx-auto max-w-lg text-center '>
			<h1 className='font-bold text-xl'>AI Assisted Connect 4</h1>
			<p>Kaylee Groves, Jorge Torrez, Brian Ramos, Christian Walsh</p>
			<div className='max-w-xs mx-auto mt-5'>
				<div className='bg-blue-500 flex flex-col w-full gap-1 p-1'>
					{board.map((row, i) => (
						<div key={i} className='bg-blue-500 gap-1 grid grid-cols-6'>
							{row.map((col, j) => (
								<div className='flex flex-col'>
									<div
										key={j}
										className='aspect-square flex items-center justify-center rounded-full group'
										style={{ backgroundColor: col === ' ' ? 'white' : col === 'O' ? 'red' : 'yellow' }}
									>
										<span className='group-hover:opacity-100 opacity-0'>{col}</span>
									</div>
								</div>
							))}
						</div>
					))}
					{!winningPlayer && (
						<div className='grid grid-cols-6'>
							{Array.from({ length: 6 }).map((_, j) => (
								<button
									disabled={!openLocations.includes(j)}
									className='disabled:opacity-20 group text-white rounded hover:bg-black/25'
									onClick={() => makeMove(j)}
									style={{ backgroundColor: currentSuggestion?.top_suggestion.column === j ? 'orange' : 'transparent' }}
								>
									<span className='group-hover:hidden'>{j}</span>
									<span className='group-hover:block hidden'>↑</span>
								</button>
							))}
						</div>
					)}
					<h1 className='bg-green-500 text-white'>{winningPlayer && <>Game won by {winningPlayer}!!</>}</h1>
				</div>
				{!winningPlayer && (
					<>
						{currentSuggestion?.column_scores && (
							<div className='grid grid-cols-6'>
								{Array.from({ length: 6 }).map((_, index) => (
									<div className='bg-neutral-200 text-xs py-2'>{currentSuggestion?.column_scores[index] ?? 'I'}</div>
								))}
							</div>
						)}
						<div className='mt-2'>
							<b>Current player: {currentPlayer}</b>
							<p className='text-sm'>
								Suggestion: Drop into column {currentSuggestion?.top_suggestion.column} (score:{' '}
								{currentSuggestion?.top_suggestion.score})
							</p>
						</div>
					</>
				)}
			</div>
		</main>
	)
}
