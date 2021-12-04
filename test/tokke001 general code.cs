using System;
using FIFALibrary20;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace FIFAConverter
{
	// Token: 0x0200000D RID: 13
	public class General
	{
		// Token: 0x06000262 RID: 610 RVA: 0x0001D40F File Offset: 0x0001B60F
		public General()
		{
		}

		// Token: 0x06000263 RID: 611 RVA: 0x0001DBB4 File Offset: 0x0001BDB4
		public static General.EFileFormat GetFileFormat(General.EGameType GameType)
		{
			switch (GameType)
			{
			case General.EGameType.FIFA_06_XBOX360:
			case General.EGameType.FIFA_World_Cup_2006:
				return General.EFileFormat.RX2_OLD;
			case General.EGameType.FIFA_07_XBOX360:
			case General.EGameType.UEFA_CHAMPIONS_LEAGUE_0607:
			case General.EGameType.FIFA_08_XBOX360:
			case General.EGameType.UEFA_Euro_2008:
			case General.EGameType.FIFA_09_XBOX360:
				return General.EFileFormat.RX2;
			case General.EGameType.FIFA_10_CONSOLE:
			case General.EGameType.FIFA_World_Cup_2010_SA:
			case General.EGameType.FIFA_11_PC:
			case General.EGameType.FIFA_11_CONSOLE:
			case General.EGameType.FIFA_ONLINE_3_OLD:
				return General.EFileFormat.RX3_Hybrid;
			case General.EGameType.FIFA_17_FROSTBITE:
			case General.EGameType.FIFA_18_FROSTBITE:
			case General.EGameType.FIFA_19_FROSTBITE:
			case General.EGameType.FIFA_20_FROSTBITE:
			case General.EGameType.FIFA_21_FROSTBITE:
				return General.EFileFormat.FB;
			}
			return General.EFileFormat.RX3;
		}

		// Token: 0x06000264 RID: 612 RVA: 0x0001DC64 File Offset: 0x0001BE64
		public static General.ESkeletonType GetSkeletonType(General.EGameType GameType)
		{
			General.ESkeletonType GetSkeletonType;
			switch (GameType)
			{
			case General.EGameType.FIFA_06_XBOX360:
			case General.EGameType.FIFA_World_Cup_2006:
			case General.EGameType.FIFA_07_XBOX360:
			case General.EGameType.UEFA_CHAMPIONS_LEAGUE_0607:
			case General.EGameType.FIFA_08_XBOX360:
			case General.EGameType.UEFA_Euro_2008:
			case General.EGameType.FIFA_09_XBOX360:
				GetSkeletonType = General.ESkeletonType.OLD_SKELETON;
				break;
			case General.EGameType.FIFA_10_CONSOLE:
			case General.EGameType.FIFA_World_Cup_2010_SA:
			case General.EGameType.FIFA_11_PC:
			case General.EGameType.FIFA_ONLINE_3_OLD:
				GetSkeletonType = General.ESkeletonType.FIFA11PC_SKELETON;
				break;
			case General.EGameType.FIFA_11_CONSOLE:
			case General.EGameType.FIFA_12:
			case General.EGameType.FIFA_13:
			case General.EGameType.FIFA_ONLINE_3_NEW:
			case General.EGameType.FIFA_Street_2012:
			case General.EGameType.PS_VITA:
				GetSkeletonType = General.ESkeletonType.IE_SKELETON;
				break;
			case General.EGameType.FIFA_14:
			case General.EGameType.FIFA_World_Cup_2014:
			case General.EGameType.FIFA_17_PS3_XBOX360:
			case General.EGameType.FIFA_18_PS3_XBOX360:
			case General.EGameType.FIFA_19_PS3_XBOX360:
			case General.EGameType.FIFA_18_Switch:
			case General.EGameType.FIFA_19_Switch:
			case General.EGameType.FIFA_20_Switch:
			case General.EGameType.FIFA_21_Switch:
				GetSkeletonType = General.ESkeletonType.FIFA14_SKELETON;
				break;
			case General.EGameType.FIFA_15:
				GetSkeletonType = General.ESkeletonType.FIFA15_SKELETON;
				break;
			case General.EGameType.FIFA_16:
				GetSkeletonType = General.ESkeletonType.FIFA16_SKELETON;
				break;
			case General.EGameType.FIFA_17_FROSTBITE:
			case General.EGameType.FIFA_18_FROSTBITE:
			case General.EGameType.FIFA_19_FROSTBITE:
			case General.EGameType.FIFA_20_FROSTBITE:
			case General.EGameType.FIFA_21_FROSTBITE:
			case General.EGameType.FIFA_ONLINE_4_NEW:
				GetSkeletonType = General.ESkeletonType.FROSTBITE_NEW_SKELETON;
				break;
			case General.EGameType.FIFA_ONLINE_4_OLD:
				GetSkeletonType = General.ESkeletonType.FROSTBITE_OLD_SKELETON;
				break;
			default:
				GetSkeletonType = (General.ESkeletonType)0;
				break;
			}
			return GetSkeletonType;
		}

		// Token: 0x06000265 RID: 613 RVA: 0x0001DD3C File Offset: 0x0001BF3C
		public static General.ENeckType GetHeadModelNeckType(General.EGameType GameType)
		{
			General.ENeckType GetHeadModelNeckType;
			switch (GameType)
			{
			case General.EGameType.FIFA_06_XBOX360:
			case General.EGameType.FIFA_World_Cup_2006:
			case General.EGameType.FIFA_07_XBOX360:
			case General.EGameType.UEFA_CHAMPIONS_LEAGUE_0607:
			case General.EGameType.FIFA_08_XBOX360:
			case General.EGameType.UEFA_Euro_2008:
			case General.EGameType.FIFA_09_XBOX360:
			case General.EGameType.FIFA_10_CONSOLE:
			case General.EGameType.FIFA_World_Cup_2010_SA:
				GetHeadModelNeckType = General.ENeckType.TYPE1_OLD;
				break;
			case General.EGameType.FIFA_11_PC:
			case General.EGameType.FIFA_11_CONSOLE:
			case General.EGameType.FIFA_12:
			case General.EGameType.FIFA_13:
			case General.EGameType.FIFA_14:
			case General.EGameType.FIFA_World_Cup_2014:
			case General.EGameType.FIFA_ONLINE_3_OLD:
			case General.EGameType.FIFA_ONLINE_3_NEW:
			case General.EGameType.FIFA_Street_2012:
			case General.EGameType.PS_VITA:
				GetHeadModelNeckType = General.ENeckType.TYPE2;
				break;
			case General.EGameType.FIFA_15:
			case General.EGameType.FIFA_16:
				GetHeadModelNeckType = General.ENeckType.TYPE3;
				break;
			case General.EGameType.FIFA_17_FROSTBITE:
			case General.EGameType.FIFA_18_FROSTBITE:
			case General.EGameType.FIFA_19_FROSTBITE:
			case General.EGameType.FIFA_20_FROSTBITE:
			case General.EGameType.FIFA_21_FROSTBITE:
			case General.EGameType.FIFA_17_PS3_XBOX360:
			case General.EGameType.FIFA_18_PS3_XBOX360:
			case General.EGameType.FIFA_19_PS3_XBOX360:
			case General.EGameType.FIFA_18_Switch:
			case General.EGameType.FIFA_19_Switch:
			case General.EGameType.FIFA_20_Switch:
			case General.EGameType.FIFA_21_Switch:
			case General.EGameType.FIFA_ONLINE_4_OLD:
			case General.EGameType.FIFA_ONLINE_4_NEW:
				GetHeadModelNeckType = General.ENeckType.TYPE4_NEW;
				break;
			default:
				GetHeadModelNeckType = General.ENeckType.TYPE2;
				break;
			}
			return GetHeadModelNeckType;
		}

		// Token: 0x06000266 RID: 614 RVA: 0x0001DE00 File Offset: 0x0001C000
		public static General.EFileType GetFileType(Rx2File m_Rx2File, string FileName = "")
		{
			string StrName = General.GetNameString(m_Rx2File);
			bool flag = General.IsHeadModelFile(StrName);
			General.EFileType GetFileType;
			if (flag)
			{
				GetFileType = General.EFileType.HEAD_MODEL;
			}
			else
			{
				bool flag2 = General.IsBallModelFile(StrName);
				if (flag2)
				{
					GetFileType = General.EFileType.BALL_MODEL;
				}
				else
				{
					bool flag3 = General.IsHairModelFile(StrName);
					if (flag3)
					{
						GetFileType = General.EFileType.HAIR_MODEL;
					}
					else
					{
						bool flag4 = General.IsHairLodModelFile(StrName);
						if (flag4)
						{
							GetFileType = General.EFileType.HAIR_LOD_MODEL;
						}
						else
						{
							bool flag5 = General.IsShoeModelFile(StrName);
							if (flag5)
							{
								GetFileType = General.EFileType.SHOE_MODEL;
							}
							else
							{
								bool flag6 = General.IsHeadLodModelFile(StrName);
								if (flag6)
								{
									GetFileType = General.EFileType.HEAD_LOD_MODEL;
								}
								else
								{
									bool flag7 = General.IsGkPantsModelFile(StrName);
									if (flag7)
									{
										GetFileType = General.EFileType.GKPANTS_MODEL;
									}
									else
									{
										bool flag8 = FileName.Contains("_");
										if (flag8)
										{
											FileName = Strings.Mid(FileName, 1, checked(Strings.InStr(FileName, "_", CompareMethod.Binary) - 1));
										}
										string text = FileName;
										uint num = <PrivateImplementationDetails>.ComputeStringHash(text);
										if (num <= 1941466512U)
										{
											if (num <= 424490508U)
											{
												if (num != 223492821U)
												{
													if (num != 424490508U)
													{
														goto IL_1F7;
													}
													if (Operators.CompareString(text, "legs", false) != 0)
													{
														goto IL_1F7;
													}
													return General.EFileType.LEGS_MODEL;
												}
												else
												{
													if (Operators.CompareString(text, "sock", false) != 0)
													{
														goto IL_1F7;
													}
													goto IL_1EB;
												}
											}
											else if (num != 912390822U)
											{
												if (num != 1941466512U)
												{
													goto IL_1F7;
												}
												if (Operators.CompareString(text, "gkglove", false) != 0)
												{
													goto IL_1F7;
												}
												return General.EFileType.GKGLOVE_MODEL;
											}
											else if (Operators.CompareString(text, "shoeslod", false) != 0)
											{
												goto IL_1F7;
											}
										}
										else if (num <= 2658292562U)
										{
											if (num != 2633735346U)
											{
												if (num != 2658292562U)
												{
													goto IL_1F7;
												}
												if (Operators.CompareString(text, "socks", false) != 0)
												{
													goto IL_1F7;
												}
												goto IL_1EB;
											}
											else
											{
												if (Operators.CompareString(text, "arms", false) != 0)
												{
													goto IL_1F7;
												}
												return General.EFileType.ARMS_MODEL;
											}
										}
										else if (num != 3003550291U)
										{
											if (num != 3276725531U)
											{
												goto IL_1F7;
											}
											if (Operators.CompareString(text, "shoeslod_low", false) != 0)
											{
												goto IL_1F7;
											}
										}
										else if (Operators.CompareString(text, "shoes", false) != 0)
										{
											goto IL_1F7;
										}
										return General.EFileType.SHOE_MODEL;
										IL_1EB:
										return General.EFileType.SOCK_MODEL;
										IL_1F7:
										GetFileType = General.EFileType.OTHER;
									}
								}
							}
						}
					}
				}
			}
			return GetFileType;
		}

		// Token: 0x06000267 RID: 615 RVA: 0x0001E00C File Offset: 0x0001C20C
		public static General.EFileType GetFileType(Rx3File m_Rx3File, string FileName = "")
		{
			string StrName = General.GetNameString(m_Rx3File);
			bool flag = General.IsHeadModelFile(StrName);
			General.EFileType GetFileType;
			if (flag)
			{
				GetFileType = General.EFileType.HEAD_MODEL;
			}
			else
			{
				bool flag2 = General.IsBallModelFile(StrName);
				if (flag2)
				{
					GetFileType = General.EFileType.BALL_MODEL;
				}
				else
				{
					bool flag3 = General.IsHairModelFile(StrName);
					if (flag3)
					{
						GetFileType = General.EFileType.HAIR_MODEL;
					}
					else
					{
						bool flag4 = General.IsHairLodModelFile(StrName);
						if (flag4)
						{
							GetFileType = General.EFileType.HAIR_LOD_MODEL;
						}
						else
						{
							bool flag5 = General.IsShoeModelFile(StrName);
							if (flag5)
							{
								GetFileType = General.EFileType.SHOE_MODEL;
							}
							else
							{
								bool flag6 = General.IsHeadLodModelFile(StrName);
								if (flag6)
								{
									GetFileType = General.EFileType.HEAD_LOD_MODEL;
								}
								else
								{
									bool flag7 = General.IsGkPantsModelFile(StrName);
									if (flag7)
									{
										GetFileType = General.EFileType.GKPANTS_MODEL;
									}
									else
									{
										bool flag8 = FileName.Contains("_");
										if (flag8)
										{
											FileName = Strings.Mid(FileName, 1, checked(Strings.InStr(FileName, "_", CompareMethod.Binary) - 1));
										}
										string text = FileName;
										uint num = <PrivateImplementationDetails>.ComputeStringHash(text);
										if (num <= 1941466512U)
										{
											if (num <= 424490508U)
											{
												if (num != 223492821U)
												{
													if (num != 424490508U)
													{
														goto IL_1F7;
													}
													if (Operators.CompareString(text, "legs", false) != 0)
													{
														goto IL_1F7;
													}
													return General.EFileType.LEGS_MODEL;
												}
												else
												{
													if (Operators.CompareString(text, "sock", false) != 0)
													{
														goto IL_1F7;
													}
													goto IL_1EB;
												}
											}
											else if (num != 912390822U)
											{
												if (num != 1941466512U)
												{
													goto IL_1F7;
												}
												if (Operators.CompareString(text, "gkglove", false) != 0)
												{
													goto IL_1F7;
												}
												return General.EFileType.GKGLOVE_MODEL;
											}
											else if (Operators.CompareString(text, "shoeslod", false) != 0)
											{
												goto IL_1F7;
											}
										}
										else if (num <= 2658292562U)
										{
											if (num != 2633735346U)
											{
												if (num != 2658292562U)
												{
													goto IL_1F7;
												}
												if (Operators.CompareString(text, "socks", false) != 0)
												{
													goto IL_1F7;
												}
												goto IL_1EB;
											}
											else
											{
												if (Operators.CompareString(text, "arms", false) != 0)
												{
													goto IL_1F7;
												}
												return General.EFileType.ARMS_MODEL;
											}
										}
										else if (num != 3003550291U)
										{
											if (num != 3276725531U)
											{
												goto IL_1F7;
											}
											if (Operators.CompareString(text, "shoeslod_low", false) != 0)
											{
												goto IL_1F7;
											}
										}
										else if (Operators.CompareString(text, "shoes", false) != 0)
										{
											goto IL_1F7;
										}
										return General.EFileType.SHOE_MODEL;
										IL_1EB:
										return General.EFileType.SOCK_MODEL;
										IL_1F7:
										GetFileType = General.EFileType.OTHER;
									}
								}
							}
						}
					}
				}
			}
			return GetFileType;
		}

		// Token: 0x06000268 RID: 616 RVA: 0x0001E218 File Offset: 0x0001C418
		private static string GetNameString(Rx2File m_model_in)
		{
			bool flag = m_model_in.RW4Section != null && m_model_in.RW4Section.RW4NameSection != null && m_model_in.RW4Section.RW4NameSection.NumNames > 0;
			checked
			{
				if (flag)
				{
					int num = (int)(m_model_in.RW4Section.RW4NameSection.NumNames - 1);
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = m_model_in.RW4Section.RW4NameSection.Names[i].ObjectId == RWSectionCode.EA_FxShader_FxRenderableSimple;
						if (flag2)
						{
							return m_model_in.RW4Section.RW4NameSection.Names[i].Name;
						}
					}
				}
				else
				{
					bool flag3 = m_model_in.RW4Section != null && m_model_in.RW4Section.RW4Shader_FxRenderableSimples != null;
					if (flag3)
					{
						return m_model_in.RW4Section.RW4Shader_FxRenderableSimples[0].String_1;
					}
				}
				return "";
			}
		}

		// Token: 0x06000269 RID: 617 RVA: 0x0001E2F4 File Offset: 0x0001C4F4
		private static string GetNameString(Rx3File m_model_in)
		{
			bool flag = m_model_in.RW4Section != null && m_model_in.RW4Section.RW4NameSection != null && m_model_in.RW4Section.RW4NameSection.NumNames > 0;
			checked
			{
				if (flag)
				{
					int num = (int)(m_model_in.RW4Section.RW4NameSection.NumNames - 1);
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = m_model_in.RW4Section.RW4NameSection.Names[i].ObjectId == RWSectionCode.EA_FxShader_FxRenderableSimple;
						if (flag2)
						{
							return m_model_in.RW4Section.RW4NameSection.Names[i].Name;
						}
					}
				}
				else
				{
					bool flag3 = m_model_in.Rx3NameTable != null && unchecked((ulong)m_model_in.Rx3NameTable.NumNames) > 0UL;
					if (flag3)
					{
						long num2 = (long)(unchecked((ulong)m_model_in.Rx3NameTable.NumNames) - 1UL);
						for (long j = 0L; j <= num2; j += 1L)
						{
							bool flag4 = m_model_in.Rx3NameTable.Names[(int)j].ObjectId == (Rx3SectionHash)3566041216U;
							if (flag4)
							{
								return m_model_in.Rx3NameTable.Names[(int)j].Name;
							}
						}
					}
					else
					{
						bool flag5 = m_model_in.RW4Section != null && m_model_in.RW4Section.RW4Shader_FxRenderableSimples != null;
						if (flag5)
						{
							return m_model_in.RW4Section.RW4Shader_FxRenderableSimples[0].String_1;
						}
					}
				}
				return "";
			}
		}

		// Token: 0x0600026A RID: 618 RVA: 0x0001E458 File Offset: 0x0001C658
		protected static bool IsHeadModelFile(string StrName)
		{
			return (StrName.Contains("eyes") | StrName.Contains("head") | StrName.Contains("eyel_") | StrName.Contains("eyer_")) & !(StrName.Contains("eyeslod") | StrName.Contains("headlod"));
		}

		// Token: 0x0600026B RID: 619 RVA: 0x0001E4C0 File Offset: 0x0001C6C0
		protected static bool IsHeadLodModelFile(string StrName)
		{
			return StrName.Contains("eyeslod") | StrName.Contains("headlod");
		}

		// Token: 0x0600026C RID: 620 RVA: 0x0001E4F4 File Offset: 0x0001C6F4
		protected static bool IsBallModelFile(string StrName)
		{
			return (StrName.Contains("ball") | StrName.Contains("Ball")) & !(StrName.Contains("ballboy") | StrName.Contains("Ballboy"));
		}

		// Token: 0x0600026D RID: 621 RVA: 0x0001E544 File Offset: 0x0001C744
		protected static bool IsHairModelFile(string StrName)
		{
			return StrName.Contains("player_hair_kk_alpha") & !StrName.Contains("player_hair_kk_alphaA_lod");
		}

		// Token: 0x0600026E RID: 622 RVA: 0x0001E57C File Offset: 0x0001C77C
		protected static bool IsHairLodModelFile(string StrName)
		{
			return StrName.Contains("player_hair_kk_alphaA_lod");
		}

		// Token: 0x0600026F RID: 623 RVA: 0x0001E5A4 File Offset: 0x0001C7A4
		protected static bool IsShoeModelFile(string StrName)
		{
			return StrName.Contains("shoe") | StrName.Contains("Shoe");
		}

		// Token: 0x06000270 RID: 624 RVA: 0x0001E5D8 File Offset: 0x0001C7D8
		protected static bool IsGkPantsModelFile(string StrName)
		{
			return StrName.Contains("gkpants");
		}

		// Token: 0x06000271 RID: 625 RVA: 0x0001E600 File Offset: 0x0001C800
		public static bool IsGameOldEngine(General.EGameType GameType)
		{
			return GameType - General.EGameType.FIFA_06_XBOX360 <= 9 || GameType == General.EGameType.FIFA_ONLINE_3_OLD;
		}

		// Token: 0x06000272 RID: 626 RVA: 0x0001E62C File Offset: 0x0001C82C
		public static bool IsGameImpactEngine(General.EGameType GameType)
		{
			return GameType - General.EGameType.FIFA_11_CONSOLE <= 2 || GameType == General.EGameType.FIFA_ONLINE_3_NEW || GameType - General.EGameType.FIFA_Street_2012 <= 1;
		}

		// Token: 0x06000273 RID: 627 RVA: 0x0001E664 File Offset: 0x0001C864
		public static bool IsGameFrostbiteEngine(General.EGameType GameType)
		{
			return General.IsGameFrostbiteEngineOld(GameType) || General.IsGameFrostbiteEngineNew(GameType);
		}

		// Token: 0x06000274 RID: 628 RVA: 0x0001E694 File Offset: 0x0001C894
		public static bool IsGameFrostbiteEngineOld(General.EGameType GameType)
		{
			return GameType == General.EGameType.FIFA_ONLINE_4_OLD;
		}

		// Token: 0x06000275 RID: 629 RVA: 0x0001E6B8 File Offset: 0x0001C8B8
		public static bool IsGameFrostbiteEngineNew(General.EGameType GameType)
		{
			return GameType - General.EGameType.FIFA_17_FROSTBITE <= 4 || GameType == General.EGameType.FIFA_ONLINE_4_NEW;
		}

		// Token: 0x06000276 RID: 630 RVA: 0x0001E6E4 File Offset: 0x0001C8E4
		public static bool IsSwitchGame(General.EGameType GameType)
		{
			return GameType - General.EGameType.FIFA_18_Switch <= 3;
		}

		// Token: 0x06000277 RID: 631 RVA: 0x0001E70C File Offset: 0x0001C90C
		public static bool HasOldNameTableFormat(General.EGameType GameType)
		{
			if (GameType <= General.EGameType.FIFA_13)
			{
				if (GameType - General.EGameType.FIFA_06_XBOX360 > 9)
				{
					if (GameType - General.EGameType.FIFA_11_CONSOLE > 2)
					{
						goto IL_33;
					}
					goto IL_2E;
				}
			}
			else if (GameType != General.EGameType.FIFA_ONLINE_3_OLD)
			{
				if (GameType != General.EGameType.FIFA_Street_2012)
				{
					goto IL_33;
				}
				goto IL_2E;
			}
			return true;
			IL_2E:
			return true;
			IL_33:
			return false;
		}

		// Token: 0x06000278 RID: 632 RVA: 0x0001E754 File Offset: 0x0001C954
		public static string EGameTypeToString(General.EGameType GameType)
		{
			string EGameTypeToString;
			switch (GameType)
			{
			case General.EGameType.FIFA_06_XBOX360:
				EGameTypeToString = "FIFA 06 (Console)";
				break;
			case General.EGameType.FIFA_World_Cup_2006:
				EGameTypeToString = "2006 FIFA World Cup";
				break;
			case General.EGameType.FIFA_07_XBOX360:
				EGameTypeToString = "FIFA 07 (Console)";
				break;
			case General.EGameType.UEFA_CHAMPIONS_LEAGUE_0607:
				EGameTypeToString = "UEFA Champions League 06–07";
				break;
			case General.EGameType.FIFA_08_XBOX360:
				EGameTypeToString = "FIFA 08 (Console)";
				break;
			case General.EGameType.UEFA_Euro_2008:
				EGameTypeToString = "UEFA Euro 2008";
				break;
			case General.EGameType.FIFA_09_XBOX360:
				EGameTypeToString = "FIFA 09 (Console)";
				break;
			case General.EGameType.FIFA_10_CONSOLE:
				EGameTypeToString = "FIFA 10 (Console)";
				break;
			case General.EGameType.FIFA_World_Cup_2010_SA:
				EGameTypeToString = "2010 FIFA World Cup SA";
				break;
			case General.EGameType.FIFA_11_PC:
				EGameTypeToString = "FIFA 11 (Pc)";
				break;
			case General.EGameType.FIFA_11_CONSOLE:
				EGameTypeToString = "FIFA 11 (Console)";
				break;
			case General.EGameType.FIFA_12:
				EGameTypeToString = "FIFA 12";
				break;
			case General.EGameType.FIFA_13:
				EGameTypeToString = "FIFA 13";
				break;
			case General.EGameType.FIFA_14:
				EGameTypeToString = "FIFA 14";
				break;
			case General.EGameType.FIFA_World_Cup_2014:
				EGameTypeToString = "2014 FIFA World Cup Brazil";
				break;
			case General.EGameType.FIFA_15:
				EGameTypeToString = "FIFA 15";
				break;
			case General.EGameType.FIFA_16:
				EGameTypeToString = "FIFA 16";
				break;
			case General.EGameType.FIFA_17_FROSTBITE:
				EGameTypeToString = "FIFA 17 (Frostbite)";
				break;
			case General.EGameType.FIFA_18_FROSTBITE:
				EGameTypeToString = "FIFA 18 (Frostbite)";
				break;
			case General.EGameType.FIFA_19_FROSTBITE:
				EGameTypeToString = "FIFA 19 (Frostbite)";
				break;
			case General.EGameType.FIFA_20_FROSTBITE:
				EGameTypeToString = "FIFA 20 (Frostbite)";
				break;
			case General.EGameType.FIFA_21_FROSTBITE:
				EGameTypeToString = "FIFA 21 (Frostbite)";
				break;
			case General.EGameType.FIFA_17_PS3_XBOX360:
				EGameTypeToString = "FIFA 17 (ps3/xbox360)";
				break;
			case General.EGameType.FIFA_18_PS3_XBOX360:
				EGameTypeToString = "FIFA 18 (ps3/xbox360)";
				break;
			case General.EGameType.FIFA_19_PS3_XBOX360:
				EGameTypeToString = "FIFA 19 (ps3/xbox360)";
				break;
			case General.EGameType.FIFA_18_Switch:
				EGameTypeToString = "FIFA 18 (Switch)";
				break;
			case General.EGameType.FIFA_19_Switch:
				EGameTypeToString = "FIFA 19 (Switch)";
				break;
			case General.EGameType.FIFA_20_Switch:
				EGameTypeToString = "FIFA 20 (Switch)";
				break;
			case General.EGameType.FIFA_21_Switch:
				EGameTypeToString = "FIFA 21 (Switch)";
				break;
			case General.EGameType.FIFA_ONLINE_3_OLD:
				EGameTypeToString = "FIFA Online 3 (Old engine)";
				break;
			case General.EGameType.FIFA_ONLINE_3_NEW:
				EGameTypeToString = "FIFA Online 3 (New engine)";
				break;
			case General.EGameType.FIFA_ONLINE_4_OLD:
				EGameTypeToString = "FIFA Online 4 (Old)";
				break;
			case General.EGameType.FIFA_ONLINE_4_NEW:
				EGameTypeToString = "FIFA Online 4 (New)";
				break;
			case General.EGameType.FIFA_Street_2012:
				EGameTypeToString = "FIFA Street (2012)";
				break;
			case General.EGameType.PS_VITA:
				EGameTypeToString = "PS Vita";
				break;
			default:
				EGameTypeToString = GameType.ToString();
				break;
			}
			return EGameTypeToString;
		}

		// Token: 0x06000279 RID: 633 RVA: 0x0001E990 File Offset: 0x0001CB90
		public static General.EGameType StringToEGameType(string GameType)
		{
			uint num = <PrivateImplementationDetails>.ComputeStringHash(GameType);
			if (num <= 2597688246U)
			{
				if (num <= 1662386307U)
				{
					if (num <= 944465409U)
					{
						if (num <= 462616133U)
						{
							if (num != 338727733U)
							{
								if (num == 462616133U)
								{
									if (Operators.CompareString(GameType, "FIFA 21 (Switch)", false) == 0)
									{
										return General.EGameType.FIFA_21_Switch;
									}
								}
							}
							else if (Operators.CompareString(GameType, "FIFA 21 (Frostbite)", false) == 0)
							{
								return General.EGameType.FIFA_21_FROSTBITE;
							}
						}
						else if (num != 745368203U)
						{
							if (num == 944465409U)
							{
								if (Operators.CompareString(GameType, "FIFA 11 (Console)", false) == 0)
								{
									return General.EGameType.FIFA_11_CONSOLE;
								}
							}
						}
						else if (Operators.CompareString(GameType, "FIFA 08 (Console)", false) == 0)
						{
							return General.EGameType.FIFA_08_XBOX360;
						}
					}
					else if (num <= 1226536659U)
					{
						if (num != 1105473540U)
						{
							if (num == 1226536659U)
							{
								if (Operators.CompareString(GameType, "FIFA Online 3 (Old engine)", false) == 0)
								{
									return General.EGameType.FIFA_ONLINE_3_OLD;
								}
							}
						}
						else if (Operators.CompareString(GameType, "FIFA Street (2012)", false) == 0)
						{
							return General.EGameType.FIFA_Street_2012;
						}
					}
					else if (num != 1457711674U)
					{
						if (num == 1662386307U)
						{
							if (Operators.CompareString(GameType, "UEFA Euro 2008", false) == 0)
							{
								return General.EGameType.UEFA_Euro_2008;
							}
						}
					}
					else if (Operators.CompareString(GameType, "FIFA 19 (Frostbite)", false) == 0)
					{
						return General.EGameType.FIFA_19_FROSTBITE;
					}
				}
				else if (num <= 2331996204U)
				{
					if (num <= 1896142494U)
					{
						if (num != 1742674011U)
						{
							if (num == 1896142494U)
							{
								if (Operators.CompareString(GameType, "FIFA 20 (Frostbite)", false) == 0)
								{
									return General.EGameType.FIFA_20_FROSTBITE;
								}
							}
						}
						else if (Operators.CompareString(GameType, "FIFA 17 (ps3/xbox360)", false) == 0)
						{
							return General.EGameType.FIFA_17_PS3_XBOX360;
						}
					}
					else if (num != 2225839957U)
					{
						if (num == 2331996204U)
						{
							if (Operators.CompareString(GameType, "FIFA Online 3 (New engine)", false) == 0)
							{
								return General.EGameType.FIFA_ONLINE_3_NEW;
							}
						}
					}
					else if (Operators.CompareString(GameType, "UEFA Champions League 06–07", false) == 0)
					{
						return General.EGameType.UEFA_CHAMPIONS_LEAGUE_0607;
					}
				}
				else if (num <= 2481611920U)
				{
					if (num != 2467992620U)
					{
						if (num == 2481611920U)
						{
							if (Operators.CompareString(GameType, "FIFA 09 (Console)", false) == 0)
							{
								return General.EGameType.FIFA_09_XBOX360;
							}
						}
					}
					else if (Operators.CompareString(GameType, "FIFA Online 4 (Old)", false) == 0)
					{
						return General.EGameType.FIFA_ONLINE_4_OLD;
					}
				}
				else if (num != 2531613617U)
				{
					if (num != 2563108446U)
					{
						if (num == 2597688246U)
						{
							if (Operators.CompareString(GameType, "FIFA 18 (ps3/xbox360)", false) == 0)
							{
								return General.EGameType.FIFA_18_PS3_XBOX360;
							}
						}
					}
					else if (Operators.CompareString(GameType, "2010 FIFA World Cup SA", false) == 0)
					{
						return General.EGameType.FIFA_World_Cup_2010_SA;
					}
				}
				else if (Operators.CompareString(GameType, "FIFA 18 (Switch)", false) == 0)
				{
					return General.EGameType.FIFA_18_Switch;
				}
			}
			else if (num <= 3142792721U)
			{
				if (num <= 2832574014U)
				{
					if (num <= 2764998787U)
					{
						if (num != 2703844100U)
						{
							if (num == 2764998787U)
							{
								if (Operators.CompareString(GameType, "2006 FIFA World Cup", false) == 0)
								{
									return General.EGameType.FIFA_World_Cup_2006;
								}
							}
						}
						else if (Operators.CompareString(GameType, "2014 FIFA World Cup Brazil", false) == 0)
						{
							return General.EGameType.FIFA_World_Cup_2014;
						}
					}
					else if (num != 2774962948U)
					{
						if (num == 2832574014U)
						{
							if (Operators.CompareString(GameType, "FIFA 07 (Console)", false) == 0)
							{
								return General.EGameType.FIFA_07_XBOX360;
							}
						}
					}
					else if (Operators.CompareString(GameType, "FIFA 17 (Frostbite)", false) == 0)
					{
						return General.EGameType.FIFA_17_FROSTBITE;
					}
				}
				else if (num <= 2949305967U)
				{
					if (num != 2875823201U)
					{
						if (num == 2949305967U)
						{
							if (Operators.CompareString(GameType, "FIFA 11 (Pc)", false) == 0)
							{
								return General.EGameType.FIFA_11_PC;
							}
						}
					}
					else if (Operators.CompareString(GameType, "FIFA 19 (ps3/xbox360)", false) == 0)
					{
						return General.EGameType.FIFA_19_PS3_XBOX360;
					}
				}
				else if (num != 3092459864U)
				{
					if (num != 3126015102U)
					{
						if (num == 3142792721U)
						{
							if (Operators.CompareString(GameType, "FIFA 15", false) == 0)
							{
								return General.EGameType.FIFA_15;
							}
						}
					}
					else if (Operators.CompareString(GameType, "FIFA 14", false) == 0)
					{
						return General.EGameType.FIFA_14;
					}
				}
				else if (Operators.CompareString(GameType, "FIFA 16", false) == 0)
				{
					return General.EGameType.FIFA_16;
				}
			}
			else if (num <= 3835357833U)
			{
				if (num <= 3176347959U)
				{
					if (num != 3159570340U)
					{
						if (num == 3176347959U)
						{
							if (Operators.CompareString(GameType, "FIFA 13", false) == 0)
							{
								return General.EGameType.FIFA_13;
							}
						}
					}
					else if (Operators.CompareString(GameType, "FIFA 12", false) == 0)
					{
						return General.EGameType.FIFA_12;
					}
				}
				else if (num != 3442990936U)
				{
					if (num == 3835357833U)
					{
						if (Operators.CompareString(GameType, "FIFA 06 (Console)", false) == 0)
						{
							return General.EGameType.FIFA_06_XBOX360;
						}
					}
				}
				else if (Operators.CompareString(GameType, "FIFA 19 (Switch)", false) == 0)
				{
					return General.EGameType.FIFA_19_Switch;
				}
			}
			else if (num <= 3903733229U)
			{
				if (num != 3871486508U)
				{
					if (num == 3903733229U)
					{
						if (Operators.CompareString(GameType, "FIFA Online 4 (New)", false) == 0)
						{
							return General.EGameType.FIFA_ONLINE_4_NEW;
						}
					}
				}
				else if (Operators.CompareString(GameType, "FIFA 20 (Switch)", false) == 0)
				{
					return General.EGameType.FIFA_20_Switch;
				}
			}
			else if (num != 3927500865U)
			{
				if (num != 4020404374U)
				{
					if (num == 4046214710U)
					{
						if (Operators.CompareString(GameType, "PS Vita", false) == 0)
						{
							return General.EGameType.PS_VITA;
						}
					}
				}
				else if (Operators.CompareString(GameType, "FIFA 10 (Console)", false) == 0)
				{
					return General.EGameType.FIFA_10_CONSOLE;
				}
			}
			else if (Operators.CompareString(GameType, "FIFA 18 (Frostbite)", false) == 0)
			{
				return General.EGameType.FIFA_18_FROSTBITE;
			}
			return General.EGameType.UNKNOWN;
		}

		// Token: 0x0600027A RID: 634 RVA: 0x0001F01C File Offset: 0x0001D21C
		public static General.EBoneSide GetBoneSide(float X_Value)
		{
			bool flag = X_Value < 0f;
			General.EBoneSide GetBoneSide;
			if (flag)
			{
				GetBoneSide = General.EBoneSide.Left;
			}
			else
			{
				bool flag2 = X_Value > 0f;
				if (flag2)
				{
					GetBoneSide = General.EBoneSide.Right;
				}
				else
				{
					GetBoneSide = General.EBoneSide.Middle;
				}
			}
			return GetBoneSide;
		}

		// Token: 0x0200001E RID: 30
		public enum EFileFormat : byte
		{
			// Token: 0x04000156 RID: 342
			RX2_OLD = 1,
			// Token: 0x04000157 RID: 343
			RX2,
			// Token: 0x04000158 RID: 344
			RX3_Hybrid,
			// Token: 0x04000159 RID: 345
			RX3,
			// Token: 0x0400015A RID: 346
			FB
		}

		// Token: 0x0200001F RID: 31
		public enum ESkeletonType : byte
		{
			// Token: 0x0400015C RID: 348
			OLD_SKELETON = 1,
			// Token: 0x0400015D RID: 349
			FIFA11PC_SKELETON,
			// Token: 0x0400015E RID: 350
			IE_SKELETON,
			// Token: 0x0400015F RID: 351
			FIFA14_SKELETON,
			// Token: 0x04000160 RID: 352
			FIFA15_SKELETON,
			// Token: 0x04000161 RID: 353
			FIFA16_SKELETON,
			// Token: 0x04000162 RID: 354
			FROSTBITE_OLD_SKELETON,
			// Token: 0x04000163 RID: 355
			FROSTBITE_NEW_SKELETON
		}

		// Token: 0x02000020 RID: 32
		public enum ENeckType : byte
		{
			// Token: 0x04000165 RID: 357
			TYPE1_OLD = 1,
			// Token: 0x04000166 RID: 358
			TYPE2,
			// Token: 0x04000167 RID: 359
			TYPE3,
			// Token: 0x04000168 RID: 360
			TYPE4_NEW
		}

		// Token: 0x02000021 RID: 33
		public enum EFileType : byte
		{
			// Token: 0x0400016A RID: 362
			OTHER,
			// Token: 0x0400016B RID: 363
			HEAD_MODEL,
			// Token: 0x0400016C RID: 364
			HAIR_MODEL,
			// Token: 0x0400016D RID: 365
			HEAD_LOD_MODEL,
			// Token: 0x0400016E RID: 366
			HAIR_LOD_MODEL,
			// Token: 0x0400016F RID: 367
			SHOE_MODEL,
			// Token: 0x04000170 RID: 368
			SHOE_LOD_MODEL,
			// Token: 0x04000171 RID: 369
			BALL_MODEL,
			// Token: 0x04000172 RID: 370
			ARMS_MODEL,
			// Token: 0x04000173 RID: 371
			GKGLOVE_MODEL,
			// Token: 0x04000174 RID: 372
			SOCK_MODEL,
			// Token: 0x04000175 RID: 373
			LEGS_MODEL,
			// Token: 0x04000176 RID: 374
			GKPANTS_MODEL
		}

		// Token: 0x02000022 RID: 34
		public enum EGameType
		{
			// Token: 0x04000178 RID: 376
			UNKNOWN,
			// Token: 0x04000179 RID: 377
			FIFA_06_XBOX360,
			// Token: 0x0400017A RID: 378
			FIFA_World_Cup_2006,
			// Token: 0x0400017B RID: 379
			FIFA_07_XBOX360,
			// Token: 0x0400017C RID: 380
			UEFA_CHAMPIONS_LEAGUE_0607,
			// Token: 0x0400017D RID: 381
			FIFA_08_XBOX360,
			// Token: 0x0400017E RID: 382
			UEFA_Euro_2008,
			// Token: 0x0400017F RID: 383
			FIFA_09_XBOX360,
			// Token: 0x04000180 RID: 384
			FIFA_10_CONSOLE,
			// Token: 0x04000181 RID: 385
			FIFA_World_Cup_2010_SA,
			// Token: 0x04000182 RID: 386
			FIFA_11_PC,
			// Token: 0x04000183 RID: 387
			FIFA_11_CONSOLE,
			// Token: 0x04000184 RID: 388
			FIFA_12,
			// Token: 0x04000185 RID: 389
			FIFA_13,
			// Token: 0x04000186 RID: 390
			FIFA_14,
			// Token: 0x04000187 RID: 391
			FIFA_World_Cup_2014,
			// Token: 0x04000188 RID: 392
			FIFA_15,
			// Token: 0x04000189 RID: 393
			FIFA_16,
			// Token: 0x0400018A RID: 394
			FIFA_17_FROSTBITE,
			// Token: 0x0400018B RID: 395
			FIFA_18_FROSTBITE,
			// Token: 0x0400018C RID: 396
			FIFA_19_FROSTBITE,
			// Token: 0x0400018D RID: 397
			FIFA_20_FROSTBITE,
			// Token: 0x0400018E RID: 398
			FIFA_21_FROSTBITE,
			// Token: 0x0400018F RID: 399
			FIFA_17_PS3_XBOX360,
			// Token: 0x04000190 RID: 400
			FIFA_18_PS3_XBOX360,
			// Token: 0x04000191 RID: 401
			FIFA_19_PS3_XBOX360,
			// Token: 0x04000192 RID: 402
			FIFA_18_Switch,
			// Token: 0x04000193 RID: 403
			FIFA_19_Switch,
			// Token: 0x04000194 RID: 404
			FIFA_20_Switch,
			// Token: 0x04000195 RID: 405
			FIFA_21_Switch,
			// Token: 0x04000196 RID: 406
			FIFA_ONLINE_3_OLD,
			// Token: 0x04000197 RID: 407
			FIFA_ONLINE_3_NEW,
			// Token: 0x04000198 RID: 408
			FIFA_ONLINE_4_OLD,
			// Token: 0x04000199 RID: 409
			FIFA_ONLINE_4_NEW,
			// Token: 0x0400019A RID: 410
			FIFA_Street_2012,
			// Token: 0x0400019B RID: 411
			PS_VITA
		}

		// Token: 0x02000023 RID: 35
		public enum EBoneSide
		{
			// Token: 0x0400019D RID: 413
			Left = -1,
			// Token: 0x0400019E RID: 414
			Middle,
			// Token: 0x0400019F RID: 415
			Right
		}
	}
}
