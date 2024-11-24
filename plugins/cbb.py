from pyrogram import __version__
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from config import PRICE1, PRICE2, PRICE3, PRICE4, PRICE5, UPI_ID, UPI_IMAGE_URL, SCREENSHOT_URL, PAYMENT_LOGS


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    data = query.data

    if data == "about":
        await query.message.edit_text(
            text="<b>Welcome to the Premium Bot!</b>\n\nThis bot allows you to access premium features with flexible plans.",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close")
                    ]
                ]
            )
        )

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except Exception:
            pass

    elif data == "buy_prem":
        await query.message.edit_text(
            text=(
                f"👋 {query.from_user.username}\n\n"
                f"🎖️ **Available Plans:**\n\n"
                f"● {PRICE1} INR for 7 Days Premium Membership\n"
                f"● {PRICE2} INR for 1 Month Premium Membership\n"
                f"● {PRICE3} INR for 3 Months Premium Membership\n"
                f"● {PRICE4} INR for 6 Months Premium Membership\n"
                f"● {PRICE5} INR for 1 Year Premium Membership\n\n"
                f"💵 **UPI ID:** `{UPI_ID}`\n"
                f"(Tap to copy UPI ID)\n\n"
                f"📸 **QR Code:** [Click Here to Scan]({UPI_IMAGE_URL})\n\n"
                f"**Steps to Buy Premium:**\n"
                f"1. Pay the amount according to your preferred plan to this UPI ID: `{UPI_ID}`.\n"
                f"2. Take a screenshot of your payment and share it here: @sewxiy.\n"
                f"3. Alternatively, upload the screenshot here and reply with the `/bought` command.\n\n"
                f"Your **Premium Plan** will be activated after verification."
            ),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("• Send Payment Screenshot •", url=SCREENSHOT_URL)
                    ],
                    [
                        InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close")
                    ]
                ]
            )
        )


@Client.on_message(filters.command("bought") & filters.private)
async def bought(client: Client, message):
    msg = await message.reply("⏳ **Checking...**")

    reply_to_message = message.reply_to_message
    if not reply_to_message:
        await msg.edit(
            "<b>Please reply with the screenshot of your payment for premium purchase to proceed.\n\n"
            "For example, upload your screenshot and then reply to it using the `/bought` command.</b>"
        )
        return

    if reply_to_message and reply_to_message.photo:
        await client.send_photo(
            chat_id=PAYMENT_LOGS,
            photo=reply_to_message.photo.file_id,
            caption=(
                f"<b>User Information:</b>\n"
                f"👤 **Name:** {message.from_user.first_name}\n"
                f"🆔 **User ID:** `{message.from_user.id}`\n"
                f"📛 **Username:** @{message.from_user.username or 'N/A'}\n"
                f"💬 **Mention:** {message.from_user.mention}\n\n"
                f"Payment screenshot attached."
            ),
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("• Approve •", callback_data="approve"),
                        InlineKeyboardButton("• Reject •", callback_data="reject"),
                    ],
                    [
                        InlineKeyboardButton("• ᴄʟᴏsᴇ •", callback_data="close_data")
                    ]
                ]
            )
        )
        await msg.edit("<b>Your screenshot has been sent to Admins for verification.</b>")
    else:
        await msg.edit("<b>Reply to a screenshot of your payment to proceed.</b>")
