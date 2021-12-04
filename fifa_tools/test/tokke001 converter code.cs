using System;
using System.Collections.Generic;
using System.Linq;
using FIFAConverter.My;
using FIFALibrary20;
using Microsoft.DirectX.Direct3D;
using Microsoft.VisualBasic;
using Microsoft.VisualBasic.CompilerServices;

namespace FIFAConverter
{
	// Token: 0x02000010 RID: 16
	public class ConvertModel
	{
		// Token: 0x0600028B RID: 651 RVA: 0x000364CB File Offset: 0x000346CB
		public ConvertModel()
		{
			this.ChkUpdateVFormat = true;
			this.ChkUpdateNamesTable = true;
			this.ChkMoveScale = true;
		}

		// Token: 0x0600028C RID: 652 RVA: 0x000364EC File Offset: 0x000346EC
		public Rx3File Convert(General.EGameType GameType_in, General.EGameType GameType_out, Rx2File Model_in, Rx3File Model_out, BoneInfo[] Model_in_Skeleton, BoneInfo[] Model_out_Skeleton, string FileName, ref string ErrorLog)
		{
			this.m_FileName = FileName;
			this.m_GameType_in = GameType_in;
			this.m_GameType_out = GameType_out;
			this.m_FileFormat_in = General.GetFileFormat(this.m_GameType_in);
			this.m_FileFormat_out = General.GetFileFormat(this.m_GameType_out);
			this.m_FileType = General.GetFileType(Model_in, this.m_FileName);
			this.m_ConvertBones = new ConvertBones(GameType_in, GameType_out, Model_in_Skeleton, Model_out_Skeleton, this.m_FileType);
			this.ChkUpdateVFormat = MyProject.Forms.Form1.ChkUpdateVFormat.Checked;
			this.ChkUpdateNamesTable = MyProject.Forms.Form1.ChkUpdateNamesTable.Checked;
			this.ChkMoveScale = MyProject.Forms.Form1.ChkMoveScale.Checked;
			General.EFileFormat fileFormat_out = this.m_FileFormat_out;
			if (fileFormat_out != General.EFileFormat.RX2)
			{
				if (fileFormat_out - General.EFileFormat.RX3_Hybrid <= 1)
				{
					return this.ConvertToRx3(Model_in, Model_out, ref ErrorLog);
				}
			}
			return null;
		}

		// Token: 0x0600028D RID: 653 RVA: 0x000365D8 File Offset: 0x000347D8
		public Rx3File Convert(General.EGameType GameType_in, General.EGameType GameType_out, Rx3File Model_in, Rx3File Model_out, BoneInfo[] Model_in_Skeleton, BoneInfo[] Model_out_Skeleton, string FileName, ref string ErrorLog)
		{
			this.m_FileName = FileName;
			this.m_GameType_in = GameType_in;
			this.m_GameType_out = GameType_out;
			this.m_FileFormat_in = General.GetFileFormat(this.m_GameType_in);
			this.m_FileFormat_out = General.GetFileFormat(this.m_GameType_out);
			this.m_FileType = General.GetFileType(Model_in, this.m_FileName);
			this.m_ConvertBones = new ConvertBones(GameType_in, GameType_out, Model_in_Skeleton, Model_out_Skeleton, this.m_FileType);
			this.ChkUpdateVFormat = MyProject.Forms.Form1.ChkUpdateVFormat.Checked;
			this.ChkUpdateNamesTable = MyProject.Forms.Form1.ChkUpdateNamesTable.Checked;
			this.ChkMoveScale = MyProject.Forms.Form1.ChkMoveScale.Checked;
			General.EFileFormat fileFormat_out = this.m_FileFormat_out;
			if (fileFormat_out != General.EFileFormat.RX2)
			{
				if (fileFormat_out - General.EFileFormat.RX3_Hybrid <= 1)
				{
					return this.ConvertToRx3(Model_in, Model_out, ref ErrorLog);
				}
			}
			return null;
		}

		// Token: 0x0600028E RID: 654 RVA: 0x000366C4 File Offset: 0x000348C4
		private Rx3File ConvertToRx3(object Model_in, Rx3File Model_out, ref string ErrorLog)
		{
			NameTable[] NameTable_in = null;
			long NumVertexBuffers_in = 0L;
			Rx2File Model_in_rx2 = new Rx2File();
			Rx3File Model_in_rx3 = new Rx3File();
			bool flag = this.m_FileFormat_in == General.EFileFormat.RX3 | this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid;
			if (flag)
			{
				Model_in_rx3 = (Rx3File)Model_in;
				bool flag2 = Model_in_rx3.Rx3VertexBuffers != null && Model_out.Rx3VertexBuffers != null;
				if (!flag2)
				{
					return null;
				}
				NumVertexBuffers_in = (long)Model_in_rx3.Rx3VertexBuffers.Length;
			}
			else
			{
				bool flag3 = this.m_FileFormat_in == General.EFileFormat.RX2;
				if (flag3)
				{
					Model_in_rx2 = (Rx2File)Model_in;
					bool flag4 = (this.m_FileFormat_out == General.EFileFormat.RX3_Hybrid & (this.m_GameType_in == General.EGameType.FIFA_07_XBOX360 | this.m_GameType_in == General.EGameType.UEFA_CHAMPIONS_LEAGUE_0607)) | this.m_FileFormat_out == General.EFileFormat.RX3;
					if (flag4)
					{
						bool flag5 = this.m_FileType == General.EFileType.HEAD_MODEL && Model_in_rx2.Rx2VertexBuffers.Length > 2;
						if (flag5)
						{
							Model_in_rx2 = this.Fix_HeadsOldToNewMesh(Model_in_rx2);
						}
						else
						{
							Model_in_rx2 = this.Fix_OldModelsToNewFormat(Model_in_rx2);
						}
						this.ChkUpdateVFormat = false;
					}
					bool flag6 = Model_in_rx2.Rx2VertexBuffers != null && Model_out.Rx3VertexBuffers != null;
					if (!flag6)
					{
						return null;
					}
					NumVertexBuffers_in = (long)Model_in_rx2.Rx2VertexBuffers.Length;
				}
			}
			long NumVertexBuffers_out = (long)Model_out.Rx3VertexBuffers.Length;
			bool flag7 = NumVertexBuffers_in != (long)Model_out.Rx3VertexBuffers.Length;
			if (flag7)
			{
				bool flag8 = !(this.m_FileFormat_in == General.EFileFormat.RX3 & (this.m_FileFormat_out == General.EFileFormat.RX2 | this.m_FileFormat_out == General.EFileFormat.RX3_Hybrid));
				if (!flag8)
				{
					MyProject.Forms.Form1.TxtErrors.Text = MyProject.Forms.Form1.TxtErrors.Text + "\r\nNumber of VertexBuffers are different from template (File " + this.m_FileName + ".rx3), file skipped";
					return null;
				}
				this.ChkUpdateVFormat = true;
				this.ChkUpdateNamesTable = true;
			}
			bool flag9 = this.m_FileFormat_in == General.EFileFormat.RX3;
			checked
			{
				if (flag9)
				{
					NameTable_in = Model_in_rx3.Rx3NameTable.GetNameTable();
				}
				else
				{
					bool flag10 = this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid;
					if (flag10)
					{
						NameTable_in = Model_in_rx3.RW4Section.RW4NameSection.GetNameTable();
					}
					else
					{
						bool flag11 = this.m_FileFormat_in == General.EFileFormat.RX2;
						if (flag11)
						{
							bool flag12 = Model_in_rx2.RW4Section.RW4NameSection != null && Model_in_rx2.RW4Section.RW4NameSection.NumNames > 0;
							if (flag12)
							{
								NameTable_in = Model_in_rx2.RW4Section.RW4NameSection.GetNameTable();
							}
							else
							{
								NameTable_in = new NameTable[Model_in_rx2.RW4Section.RW4Shader_FxRenderableSimples.Length - 1 + 1];
								int num = NameTable_in.Length - 1;
								for (int i = 0; i <= num; i++)
								{
									NameTable_in[i] = new NameTable
									{
										ObjectId = 15663108U,
										Name = Model_in_rx2.RW4Section.RW4Shader_FxRenderableSimples[i].String_1 + ".FxRenderableSimple"
									};
								}
							}
						}
					}
				}
				bool flag13 = this.m_FileFormat_out == General.EFileFormat.RX3;
				NameTable[] NameTable_out;
				List<FIFALibrary20.VertexElement[]> ListVertexElements_out;
				if (flag13)
				{
					NameTable_out = Model_out.Rx3NameTable.GetNameTable();
					ListVertexElements_out = ConvertModel.GetVertexElementList(Model_out.Rx3VertexBuffers.Length, Model_out.Rx3VertexFormats);
				}
				else
				{
					NameTable_out = Model_out.RW4Section.RW4NameSection.GetNameTable();
					ListVertexElements_out = ConvertModel.GetVertexElementList(Model_out.Rx3VertexBuffers.Length, Model_out.RW4Section.RW4VertexDescriptors);
				}
				this.Id_in = new uint[(int)(NumVertexBuffers_in - 1L) + 1];
				int num2 = this.Id_in.Length - 1;
				for (int b = 0; b <= num2; b++)
				{
					this.Id_in[b] = (uint)this.GetInputId_fromNameTable(unchecked((long)b), NameTable_in, NameTable_out);
				}
				bool flag14 = !this.ChkUpdateVFormat;
				if (flag14)
				{
					long num3 = NumVertexBuffers_in - 1L;
					for (long j = 0L; j <= num3; j += 1L)
					{
						bool VertexIsDifferent = false;
						bool flag15 = this.m_FileFormat_out == General.EFileFormat.RX3;
						if (flag15)
						{
							bool flag16 = this.m_FileFormat_in == General.EFileFormat.RX3;
							if (flag16)
							{
								VertexIsDifferent = this.VertexSize_IsDifferent(Model_out.Rx3VertexFormats[(int)j], Model_in_rx3.Rx3VertexFormats[(int)j]);
							}
							else
							{
								bool flag17 = this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid;
								if (flag17)
								{
									int id = (int)j;
									bool flag18 = j > unchecked((long)(checked(Model_in_rx3.RW4Section.RW4VertexDescriptors.Length - 1)));
									if (flag18)
									{
										id = Model_in_rx3.RW4Section.RW4VertexDescriptors.Length - 1;
									}
									VertexIsDifferent = this.VertexSize_IsDifferent(Model_out.Rx3VertexFormats[(int)j], Model_in_rx3.RW4Section.RW4VertexDescriptors[id]);
								}
								else
								{
									bool flag19 = this.m_FileFormat_in == General.EFileFormat.RX2;
									if (flag19)
									{
										int id2 = (int)j;
										bool flag20 = j > unchecked((long)(checked(Model_in_rx2.RW4Section.RW4VertexDescriptors.Length - 1)));
										if (flag20)
										{
											id2 = Model_in_rx2.RW4Section.RW4VertexDescriptors.Length - 1;
										}
										VertexIsDifferent = this.VertexSize_IsDifferent(Model_out.Rx3VertexFormats[(int)j], Model_in_rx2.RW4Section.RW4VertexDescriptors[id2]);
									}
								}
							}
						}
						else
						{
							bool flag21 = this.m_FileFormat_in == General.EFileFormat.RX3;
							if (flag21)
							{
								int id_out = (int)j;
								bool flag22 = j > unchecked((long)(checked(Model_out.RW4Section.RW4VertexDescriptors.Length - 1)));
								if (flag22)
								{
									id_out = Model_out.RW4Section.RW4VertexDescriptors.Length - 1;
								}
								VertexIsDifferent = this.VertexSize_IsDifferent(Model_in_rx3.Rx3VertexFormats[(int)j], Model_out.RW4Section.RW4VertexDescriptors[id_out]);
							}
							else
							{
								bool flag23 = this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid;
								if (flag23)
								{
									int id_in = (int)j;
									bool flag24 = j > unchecked((long)(checked(Model_in_rx3.RW4Section.RW4VertexDescriptors.Length - 1)));
									if (flag24)
									{
										id_in = Model_in_rx3.RW4Section.RW4VertexDescriptors.Length - 1;
									}
									int id_out2 = (int)j;
									bool flag25 = j > unchecked((long)(checked(Model_out.RW4Section.RW4VertexDescriptors.Length - 1)));
									if (flag25)
									{
										id_out2 = Model_out.RW4Section.RW4VertexDescriptors.Length - 1;
									}
									VertexIsDifferent = this.VertexSize_IsDifferent(Model_out.RW4Section.RW4VertexDescriptors[id_out2], Model_in_rx3.RW4Section.RW4VertexDescriptors[id_in]);
								}
								else
								{
									bool flag26 = this.m_FileFormat_in == General.EFileFormat.RX2;
									if (flag26)
									{
										int id_in2 = (int)j;
										bool flag27 = j > unchecked((long)(checked(Model_in_rx2.RW4Section.RW4VertexDescriptors.Length - 1)));
										if (flag27)
										{
											id_in2 = Model_in_rx2.RW4Section.RW4VertexDescriptors.Length - 1;
										}
										int id_out3 = (int)j;
										bool flag28 = j > unchecked((long)(checked(Model_out.RW4Section.RW4VertexDescriptors.Length - 1)));
										if (flag28)
										{
											id_out3 = Model_out.RW4Section.RW4VertexDescriptors.Length - 1;
										}
										VertexIsDifferent = this.VertexSize_IsDifferent(Model_out.RW4Section.RW4VertexDescriptors[id_out3], Model_in_rx2.RW4Section.RW4VertexDescriptors[id_in2]);
									}
								}
							}
						}
						bool flag29 = VertexIsDifferent;
						if (flag29)
						{
							MyProject.Forms.Form1.TxtErrors.Text = MyProject.Forms.Form1.TxtErrors.Text + "\r\nWarning: VertexSize Missmatch (file " + this.m_FileName + ".rx3)";
						}
					}
				}
				bool flag30 = (this.m_FileFormat_in == General.EFileFormat.RX3 | this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid) && Model_in_rx3.Rx3IndexBuffers != null;
				if (flag30)
				{
					Model_out.Rx3IndexBuffers = this.ConvertRx3IndexBuffers(Model_in_rx3.Rx3IndexBuffers);
				}
				else
				{
					bool flag31 = this.m_FileFormat_in == General.EFileFormat.RX2 && Model_in_rx2.Rx2IndexBuffers != null && Model_in_rx2.RW4Section.RW4IndexBuffers != null;
					if (flag31)
					{
						Model_out.Rx3IndexBuffers = this.ConvertRx3IndexBuffers(Model_in_rx2.Rx2IndexBuffers, Model_in_rx2.RW4Section.RW4IndexBuffers);
					}
					else
					{
						Model_out.Rx3IndexBuffers = null;
					}
				}
				bool flag32 = this.m_FileFormat_in == General.EFileFormat.RX3 && Model_in_rx3.Rx3VertexBuffers != null && ListVertexElements_out != null;
				if (flag32)
				{
					D3DDECLTYPE DataTypeBlendWeights = this.ChkUpdateVFormat ? this.GetBoneWeightsDataType(Model_in_rx3.Rx3VertexFormats[0]) : ConvertModel.GetBoneWeightsDataType(ListVertexElements_out[0]);
					Model_out.Rx3VertexBuffers = this.ConvertRx3VertexBuffers(Model_in_rx3.Rx3VertexBuffers, Model_out.Rx3VertexBuffers, ListVertexElements_out, DataTypeBlendWeights, this.ChkUpdateVFormat, this.ChkMoveScale, ref ErrorLog);
				}
				else
				{
					bool flag33 = this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid && Model_in_rx3.Rx3VertexBuffers != null && ListVertexElements_out != null;
					if (flag33)
					{
						D3DDECLTYPE DataTypeBlendWeights2 = this.ChkUpdateVFormat ? this.GetBoneWeightsDataType(Model_in_rx3.RW4Section.RW4VertexDescriptors[0]) : ConvertModel.GetBoneWeightsDataType(ListVertexElements_out[0]);
						Model_out.Rx3VertexBuffers = this.ConvertRx3VertexBuffers(Model_in_rx3.Rx3VertexBuffers, Model_out.Rx3VertexBuffers, ListVertexElements_out, DataTypeBlendWeights2, this.ChkUpdateVFormat, this.ChkMoveScale, ref ErrorLog);
					}
					else
					{
						bool flag34 = this.m_FileFormat_in == General.EFileFormat.RX2 && Model_in_rx2.Rx2VertexBuffers != null && Model_in_rx2.RW4Section.RW4VertexBuffers != null && ListVertexElements_out != null;
						if (flag34)
						{
							D3DDECLTYPE DataTypeBlendWeights3 = this.ChkUpdateVFormat ? this.GetBoneWeightsDataType(Model_in_rx2.RW4Section.RW4VertexDescriptors[0]) : ConvertModel.GetBoneWeightsDataType(ListVertexElements_out[0]);
							Model_out.Rx3VertexBuffers = this.ConvertRx3VertexBuffers(Model_in_rx2.Rx2VertexBuffers, Model_in_rx2.RW4Section.RW4VertexBuffers, Model_out.Rx3VertexBuffers, ListVertexElements_out, DataTypeBlendWeights3, this.ChkUpdateVFormat, this.ChkMoveScale, ref ErrorLog);
						}
						else
						{
							Model_out.Rx3VertexBuffers = null;
						}
					}
				}
				bool flag35 = (this.m_FileFormat_in == General.EFileFormat.RX3 & Model_in_rx3.Rx3AnimationSkins != null) | (this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid && Model_in_rx3.RW4Section.RW4AnimationSkins != null);
				if (flag35)
				{
					Model_out.Rx3BoneRemaps = this.ConvertRx3BoneRemaps(Model_in_rx3.Rx3VertexBuffers.Length);
				}
				else
				{
					bool flag36 = this.m_FileFormat_in == General.EFileFormat.RX2 && Model_in_rx2.RW4Section.RW4AnimationSkins != null;
					if (flag36)
					{
						Model_out.Rx3BoneRemaps = this.ConvertRx3BoneRemaps(Model_in_rx2.Rx2VertexBuffers.Length);
					}
					else
					{
						Model_out.Rx3BoneRemaps = null;
					}
				}
				bool flag37 = this.m_FileFormat_out == General.EFileFormat.RX3;
				if (flag37)
				{
					bool flag38 = (this.m_FileFormat_in == General.EFileFormat.RX3 && Model_in_rx3.Rx3NameTable != null) & this.ChkUpdateNamesTable;
					if (flag38)
					{
						Model_out.Rx3NameTable = this.UpdateRx3NameSection(Model_in_rx3.Rx3NameTable, Model_out.Rx3NameTable);
					}
					else
					{
						bool flag39 = (this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid && (Model_in_rx3.RW4Section.RW4NameSection != null | Model_in_rx3.RW4Section.RW4Shader_FxRenderableSimples != null)) & this.ChkUpdateNamesTable;
						if (flag39)
						{
							Model_out.Rx3NameTable = this.UpdateRx3NameSection(Model_in_rx3.RW4Section.RW4NameSection, Model_in_rx3.RW4Section.RW4Shader_FxRenderableSimples, Model_out.Rx3NameTable);
						}
						else
						{
							bool flag40 = (this.m_FileFormat_in == General.EFileFormat.RX2 && (Model_in_rx2.RW4Section.RW4NameSection != null | Model_in_rx2.RW4Section.RW4Shader_FxRenderableSimples != null)) & this.ChkUpdateNamesTable;
							if (flag40)
							{
								Model_out.Rx3NameTable = this.UpdateRx3NameSection(Model_in_rx2.RW4Section.RW4NameSection, Model_in_rx2.RW4Section.RW4Shader_FxRenderableSimples, Model_out.Rx3NameTable);
							}
						}
					}
					bool flag41 = this.m_FileFormat_in == General.EFileFormat.RX3 && Model_in_rx3.Rx3VertexFormats != null;
					if (flag41)
					{
						bool BoneIndicesHasShort_in = Model_in_rx3.Rx3AnimationSkins != null && this.CheckBoneIndicesHasShort(Model_in_rx3.Rx3AnimationSkins[0]);
						bool BoneIndicesHasShort_out = Model_out.Rx3AnimationSkins != null && this.CheckBoneIndicesHasShort(Model_out.Rx3AnimationSkins[0]);
						Rx3VertexFormat[] rx3VertexFormats = Model_in_rx3.Rx3VertexFormats;
						Rx3VertexFormat[] rx3VertexFormats2 = Model_out.Rx3VertexFormats;
						Rx3VertexBuffer[] rx3VertexBuffers = Model_out.Rx3VertexBuffers;
						Rx3VertexFormat[] rx3VertexFormats3 = this.UpdateRx3VertexFormats(rx3VertexFormats, rx3VertexFormats2, ref rx3VertexBuffers, BoneIndicesHasShort_in, BoneIndicesHasShort_out, this.ChkUpdateVFormat);
						Model_out.Rx3VertexBuffers = rx3VertexBuffers;
						Model_out.Rx3VertexFormats = rx3VertexFormats3;
					}
					else
					{
						bool flag42 = this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid && Model_in_rx3.RW4Section.RW4VertexDescriptors != null;
						if (flag42)
						{
							bool BoneIndicesHasShort_in2 = Model_in_rx3.RW4Section.RW4AnimationSkins != null && this.CheckBoneIndicesHasShort(Model_in_rx3.RW4Section.RW4AnimationSkins[0]);
							bool BoneIndicesHasShort_out2 = Model_out.Rx3AnimationSkins != null && this.CheckBoneIndicesHasShort(Model_out.Rx3AnimationSkins[0]);
							RWGObjectType_VertexDescriptor[] rw4VertexDescriptors = Model_in_rx3.RW4Section.RW4VertexDescriptors;
							Rx3VertexFormat[] rx3VertexFormats4 = Model_out.Rx3VertexFormats;
							Rx3VertexBuffer[] rx3VertexBuffers = Model_out.Rx3VertexBuffers;
							Rx3VertexFormat[] rx3VertexFormats5 = this.UpdateRx3VertexFormats(rw4VertexDescriptors, rx3VertexFormats4, ref rx3VertexBuffers, BoneIndicesHasShort_in2, BoneIndicesHasShort_out2, this.ChkUpdateVFormat);
							Model_out.Rx3VertexBuffers = rx3VertexBuffers;
							Model_out.Rx3VertexFormats = rx3VertexFormats5;
							Model_out.Rx3VertexFormats = this.Fix_NumRx3VertexFormats(Model_out.Rx3VertexFormats, Model_out.Rx3VertexBuffers.Length);
						}
						else
						{
							bool flag43 = this.m_FileFormat_in == General.EFileFormat.RX2 && Model_in_rx2.RW4Section.RW4VertexDescriptors != null;
							if (flag43)
							{
								bool BoneIndicesHasShort_in3 = Model_in_rx2.RW4Section.RW4AnimationSkins != null && this.CheckBoneIndicesHasShort(Model_in_rx2.RW4Section.RW4AnimationSkins[0]);
								bool BoneIndicesHasShort_out3 = Model_out.Rx3AnimationSkins != null && this.CheckBoneIndicesHasShort(Model_out.Rx3AnimationSkins[0]);
								RWGObjectType_VertexDescriptor[] rw4VertexDescriptors2 = Model_in_rx2.RW4Section.RW4VertexDescriptors;
								Rx3VertexFormat[] rx3VertexFormats6 = Model_out.Rx3VertexFormats;
								Rx3VertexBuffer[] rx3VertexBuffers = Model_out.Rx3VertexBuffers;
								Rx3VertexFormat[] rx3VertexFormats7 = this.UpdateRx3VertexFormats(rw4VertexDescriptors2, rx3VertexFormats6, ref rx3VertexBuffers, BoneIndicesHasShort_in3, BoneIndicesHasShort_out3, this.ChkUpdateVFormat);
								Model_out.Rx3VertexBuffers = rx3VertexBuffers;
								Model_out.Rx3VertexFormats = rx3VertexFormats7;
								Model_out.Rx3VertexFormats = this.Fix_NumRx3VertexFormats(Model_out.Rx3VertexFormats, Model_out.Rx3VertexBuffers.Length);
							}
						}
					}
					bool flag44 = this.m_FileFormat_in == General.EFileFormat.RX3 && Model_in_rx3.Rx3SimpleMeshes != null;
					if (flag44)
					{
						Model_out.Rx3SimpleMeshes = this.UpdateRx3SimpleMeshes(Model_in_rx3.Rx3SimpleMeshes);
					}
					else
					{
						bool flag45 = this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid && Model_in_rx3.RW4Section.RW4Shader_FxRenderableSimples != null;
						if (flag45)
						{
							Model_out.Rx3SimpleMeshes = this.UpdateRx3SimpleMeshes(Model_in_rx3.RW4Section.RW4Shader_FxRenderableSimples);
						}
						else
						{
							bool flag46 = this.m_FileFormat_in == General.EFileFormat.RX2 && Model_in_rx2.RW4Section.RW4Shader_FxRenderableSimples != null;
							if (flag46)
							{
								Model_out.Rx3SimpleMeshes = this.UpdateRx3SimpleMeshes(Model_in_rx2.RW4Section.RW4Shader_FxRenderableSimples);
							}
						}
					}
					bool flag47 = this.m_FileFormat_in == General.EFileFormat.RX3 && Model_in_rx3.Rx3AnimationSkins != null && Model_in_rx3.Rx3AnimationSkins.Length != Model_out.Rx3AnimationSkins.Length;
					if (flag47)
					{
						Model_out.Rx3AnimationSkins = this.Fix_NumRx3AnimationSkins(Model_out.Rx3AnimationSkins, Model_in_rx3.Rx3AnimationSkins.Length);
					}
					else
					{
						bool flag48 = this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid && Model_in_rx3.RW4Section.RW4AnimationSkins != null && Model_in_rx3.RW4Section.RW4AnimationSkins.Length != Model_out.Rx3AnimationSkins.Length;
						if (flag48)
						{
							Model_out.Rx3AnimationSkins = this.Fix_NumRx3AnimationSkins(Model_out.Rx3AnimationSkins, Model_in_rx3.RW4Section.RW4AnimationSkins.Length);
						}
						else
						{
							bool flag49 = this.m_FileFormat_in == General.EFileFormat.RX2 && Model_in_rx2.RW4Section.RW4AnimationSkins != null && Model_in_rx2.RW4Section.RW4AnimationSkins.Length != Model_out.Rx3AnimationSkins.Length;
							if (flag49)
							{
								Model_out.Rx3AnimationSkins = this.Fix_NumRx3AnimationSkins(Model_out.Rx3AnimationSkins, Model_in_rx2.RW4Section.RW4AnimationSkins.Length);
							}
						}
					}
					bool flag50 = Model_out.Rx3EdgeMeshes != null;
					if (flag50)
					{
						Model_out.Rx3EdgeMeshes = this.UpdateRx3EdgeMeshes(Model_in_rx3.Rx3EdgeMeshes, Model_out.Rx3EdgeMeshes);
					}
				}
				else
				{
					bool flag51 = this.m_FileFormat_out == General.EFileFormat.RX3_Hybrid;
					if (flag51)
					{
						bool flag52 = this.m_FileFormat_in == General.EFileFormat.RX3;
						if (flag52)
						{
							bool flag53 = Model_in_rx3.Rx3AnimationSkins != null;
							if (flag53)
							{
							}
							bool flag54 = Model_in_rx3.Rx3SimpleMeshes != null && Model_out.RW4Section.RW4Shader_FxRenderableSimples != null;
							if (flag54)
							{
								Model_out.RW4Section.RW4Shader_FxRenderableSimples = this.UpdateRW4Shader_0XEF0004(Model_in_rx3.Rx3SimpleMeshes, Model_out.RW4Section.RW4Shader_FxRenderableSimples);
							}
							bool flag55 = Model_in_rx3.Rx3NameTable != null & this.ChkUpdateNamesTable;
							if (flag55)
							{
								Model_out.RW4Section.RW4NameSection = this.UpdateRW4NameSection(Model_in_rx3.Rx3NameTable, Model_out.RW4Section.RW4NameSection);
							}
						}
						else
						{
							bool flag56 = this.m_FileFormat_in == General.EFileFormat.RX3_Hybrid && Model_in_rx3.RW4Section != null;
							if (flag56)
							{
								bool flag57 = this.ChkUpdateVFormat & this.ChkUpdateNamesTable;
								if (flag57)
								{
									Model_out.RW4Section = this.UpdateRW4Section(Model_in_rx3.RW4Section, Model_out.RW4Section);
								}
								else
								{
									Model_out.RW4Section = this.UpdateRW4Section(Model_in_rx3.RW4Section, Model_out.RW4Section);
								}
							}
							else
							{
								bool flag58 = this.m_FileFormat_in == General.EFileFormat.RX2 && Model_in_rx2.RW4Section != null;
								if (flag58)
								{
									bool flag59 = this.m_GameType_in == General.EGameType.FIFA_07_XBOX360 | this.m_GameType_in == General.EGameType.UEFA_CHAMPIONS_LEAGUE_0607;
									if (flag59)
									{
										bool flag60 = Model_in_rx2.RW4Section.RW4Shader_FxRenderableSimples != null;
										if (flag60)
										{
										}
										bool flag61 = Model_in_rx2.RW4Section.RW4NameSection != null & this.ChkUpdateNamesTable;
										if (flag61)
										{
										}
									}
									else
									{
										bool flag62 = this.ChkUpdateVFormat & this.ChkUpdateNamesTable;
										if (flag62)
										{
											Model_out.RW4Section = this.UpdateRW4Section(Model_in_rx2.RW4Section, Model_out.RW4Section);
										}
										else
										{
											Model_out.RW4Section = this.UpdateRW4Section(Model_in_rx2.RW4Section, Model_out.RW4Section);
										}
									}
								}
							}
						}
					}
				}
				bool flag63 = NumVertexBuffers_in != NumVertexBuffers_out;
				if (flag63)
				{
					Model_out.GenerateRx3SectionHeaders();
				}
				return Model_out;
			}
		}

		// Token: 0x0600028F RID: 655 RVA: 0x00037778 File Offset: 0x00035978
		private Rx2File Fix_OldModelsToNewFormat(Rx2File m_Rx2File)
		{
			m_Rx2File.RW4Section.RW4VertexDescriptors = this.FixRW4VertexDescriptorsToNew(m_Rx2File.RW4Section.RW4VertexDescriptors);
			checked
			{
				int num = m_Rx2File.RW4Section.RW4VertexBuffers.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = i <= m_Rx2File.RW4Section.RW4VertexDescriptors.Length - 1;
					if (flag)
					{
						m_Rx2File.RW4Section.RW4VertexBuffers[i].VertexSize = (ushort)m_Rx2File.RW4Section.RW4VertexDescriptors[i].VertexSize;
					}
					else
					{
						m_Rx2File.RW4Section.RW4VertexBuffers[i].VertexSize = (ushort)m_Rx2File.RW4Section.RW4VertexDescriptors[0].VertexSize;
					}
				}
				return m_Rx2File;
			}
		}

		// Token: 0x06000290 RID: 656 RVA: 0x0003782C File Offset: 0x00035A2C
		private Rx2File Fix_HeadsOldToNewMesh(Rx2File m_Rx2File)
		{
			bool flag = m_Rx2File.Rx2VertexBuffers.Length <= 2 | this.m_FileType != General.EFileType.HEAD_MODEL | this.m_GameType_out == General.EGameType.FIFA_07_XBOX360;
			checked
			{
				Rx2File Fix_HeadsOldToNewMesh;
				if (flag)
				{
					Fix_HeadsOldToNewMesh = m_Rx2File;
				}
				else
				{
					Mesh MeshEyeLeft = null;
					Mesh MeshEyeRight = null;
					Mesh MeshEyeLashes = null;
					Mesh MeshHead = null;
					Mesh MeshMouthbag = null;
					this.GetOldMeshes(m_Rx2File, ref MeshEyeLeft, ref MeshEyeRight, ref MeshEyeLashes, ref MeshHead, ref MeshMouthbag);
					Mesh[] m_meshes = this.HeadsOldToNewMesh(MeshEyeLeft, MeshEyeRight, MeshEyeLashes, MeshHead, MeshMouthbag);
					m_Rx2File.Rx2IndexBuffers = new Rx2IndexBuffer[m_meshes.Length - 1 + 1];
					m_Rx2File.Rx2VertexBuffers = new Rx2VertexBuffer[m_meshes.Length - 1 + 1];
					int num = m_meshes.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						m_Rx2File.Rx2IndexBuffers[i] = new Rx2IndexBuffer
						{
							IndexStream = m_meshes[i].Indices
						};
						m_Rx2File.Rx2VertexBuffers[i] = new Rx2VertexBuffer
						{
							Vertexes = m_meshes[i].Vertices
						};
					}
					RW4Section rw4Section;
					(rw4Section = m_Rx2File.RW4Section).RW4AnimationSkins = (ObjectType_AnimationSkin[])Utils.CopyArray(rw4Section.RW4AnimationSkins, new ObjectType_AnimationSkin[2]);
					(rw4Section = m_Rx2File.RW4Section).RW4Shader_FxRenderableSimples = (EA_FxShader_FxRenderableSimple[])Utils.CopyArray(rw4Section.RW4Shader_FxRenderableSimples, new EA_FxShader_FxRenderableSimple[2]);
					m_Rx2File.RW4Section.RW4NameSection.NumNames = 2;
					EA_ArenaDictionary rw4NameSection;
					(rw4NameSection = m_Rx2File.RW4Section.RW4NameSection).Names = (RWName[])Utils.CopyArray(rw4NameSection.Names, new RWName[2]);
					m_Rx2File.RW4Section.RW4NameSection.Names[0] = new RWName();
					m_Rx2File.RW4Section.RW4NameSection.Names[0].Name = "head_.FxRenderableSimple";
					m_Rx2File.RW4Section.RW4NameSection.Names[0].ObjectId = RWSectionCode.EA_FxShader_FxRenderableSimple;
					m_Rx2File.RW4Section.RW4NameSection.Names[0].Index = 0U;
					m_Rx2File.RW4Section.RW4NameSection.Names[1] = new RWName();
					m_Rx2File.RW4Section.RW4NameSection.Names[1].Name = "eyes_.FxRenderableSimple";
					m_Rx2File.RW4Section.RW4NameSection.Names[1].ObjectId = RWSectionCode.EA_FxShader_FxRenderableSimple;
					m_Rx2File.RW4Section.RW4NameSection.Names[1].Index = 0U;
					m_Rx2File.RW4Section.RW4VertexDescriptors = this.FixRW4VertexDescriptorsToNew(m_Rx2File.RW4Section.RW4VertexDescriptors);
					(rw4Section = m_Rx2File.RW4Section).RW4VertexBuffers = (RWGObjectType_VertexBuffer[])Utils.CopyArray(rw4Section.RW4VertexBuffers, new RWGObjectType_VertexBuffer[2]);
					m_Rx2File.RW4Section.RW4VertexBuffers[0].NumVertices = (uint)m_Rx2File.Rx2VertexBuffers[0].Vertexes.Length;
					m_Rx2File.RW4Section.RW4VertexBuffers[0].VertexSize = (ushort)m_Rx2File.RW4Section.RW4VertexDescriptors[0].VertexSize;
					m_Rx2File.RW4Section.RW4VertexBuffers[1].NumVertices = (uint)m_Rx2File.Rx2VertexBuffers[1].Vertexes.Length;
					m_Rx2File.RW4Section.RW4VertexBuffers[1].VertexSize = (ushort)m_Rx2File.RW4Section.RW4VertexDescriptors[0].VertexSize;
					(rw4Section = m_Rx2File.RW4Section).RW4IndexBuffers = (RWGObjectType_IndexBuffer[])Utils.CopyArray(rw4Section.RW4IndexBuffers, new RWGObjectType_IndexBuffer[2]);
					m_Rx2File.RW4Section.RW4IndexBuffers[0].NumIndices = (uint)m_Rx2File.Rx2IndexBuffers[0].IndexStream.Length;
					m_Rx2File.RW4Section.RW4IndexBuffers[1].NumIndices = (uint)m_Rx2File.Rx2IndexBuffers[1].IndexStream.Length;
					Fix_HeadsOldToNewMesh = m_Rx2File;
				}
				return Fix_HeadsOldToNewMesh;
			}
		}

		// Token: 0x06000291 RID: 657 RVA: 0x00037BBC File Offset: 0x00035DBC
		private void GetOldMeshes(Rx2File m_Rx2File, ref Mesh MeshEyeLeft, ref Mesh MeshEyeRight, ref Mesh MeshEyeLashes, ref Mesh MeshHead, ref Mesh MeshMouthbag)
		{
			bool flag = m_Rx2File.RW4Section != null && m_Rx2File.RW4Section.RW4NameSection != null && m_Rx2File.RW4Section.RW4NameSection.NumNames > 0;
			checked
			{
				if (flag)
				{
					int num = (int)(m_Rx2File.RW4Section.RW4NameSection.NumNames - 1);
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = m_Rx2File.RW4Section.RW4NameSection.Names[i].ObjectId == RWSectionCode.EA_FxShader_FxRenderableSimple;
						if (flag2)
						{
							bool flag3 = true;
							bool flag4 = flag3 == m_Rx2File.RW4Section.RW4NameSection.Names[i].Name.Contains("eyel_");
							if (flag4)
							{
								MeshEyeLeft = new Mesh();
								MeshEyeLeft.Indices = m_Rx2File.Rx2IndexBuffers[i].IndexStream;
								MeshEyeLeft.Vertices = m_Rx2File.Rx2VertexBuffers[i].Vertexes;
							}
							else
							{
								flag4 = (flag3 == m_Rx2File.RW4Section.RW4NameSection.Names[i].Name.Contains("eyer_"));
								if (flag4)
								{
									MeshEyeRight = new Mesh();
									MeshEyeRight.Indices = m_Rx2File.Rx2IndexBuffers[i].IndexStream;
									MeshEyeRight.Vertices = m_Rx2File.Rx2VertexBuffers[i].Vertexes;
								}
								else
								{
									flag4 = (flag3 == m_Rx2File.RW4Section.RW4NameSection.Names[i].Name.Contains("eyelashes_"));
									if (flag4)
									{
										MeshEyeLashes = new Mesh();
										MeshEyeLashes.Indices = m_Rx2File.Rx2IndexBuffers[i].IndexStream;
										MeshEyeLashes.Vertices = m_Rx2File.Rx2VertexBuffers[i].Vertexes;
									}
									else
									{
										flag4 = (flag3 == m_Rx2File.RW4Section.RW4NameSection.Names[i].Name.Contains("head_"));
										if (flag4)
										{
											MeshHead = new Mesh();
											MeshHead.Indices = m_Rx2File.Rx2IndexBuffers[i].IndexStream;
											MeshHead.Vertices = m_Rx2File.Rx2VertexBuffers[i].Vertexes;
										}
										else
										{
											flag4 = (flag3 == m_Rx2File.RW4Section.RW4NameSection.Names[i].Name.Contains("mouthbag_"));
											if (flag4)
											{
												MeshMouthbag = new Mesh();
												MeshMouthbag.Indices = m_Rx2File.Rx2IndexBuffers[i].IndexStream;
												MeshMouthbag.Vertices = m_Rx2File.Rx2VertexBuffers[i].Vertexes;
											}
										}
									}
								}
							}
						}
					}
				}
				else
				{
					bool flag5 = m_Rx2File.RW4Section != null && m_Rx2File.RW4Section.RW4Shader_FxRenderableSimples != null;
					if (flag5)
					{
						int num2 = m_Rx2File.RW4Section.RW4Shader_FxRenderableSimples.Length - 1;
						for (int j = 0; j <= num2; j++)
						{
							bool flag6 = true;
							bool flag7 = flag6 == m_Rx2File.RW4Section.RW4Shader_FxRenderableSimples[j].String_1.Contains("eyel_");
							if (flag7)
							{
								MeshEyeLeft = new Mesh();
								MeshEyeLeft.Indices = m_Rx2File.Rx2IndexBuffers[j].IndexStream;
								MeshEyeLeft.Vertices = m_Rx2File.Rx2VertexBuffers[j].Vertexes;
							}
							else
							{
								flag7 = (flag6 == m_Rx2File.RW4Section.RW4Shader_FxRenderableSimples[j].String_1.Contains("eyer_"));
								if (flag7)
								{
									MeshEyeRight = new Mesh();
									MeshEyeRight.Indices = m_Rx2File.Rx2IndexBuffers[j].IndexStream;
									MeshEyeRight.Vertices = m_Rx2File.Rx2VertexBuffers[j].Vertexes;
								}
								else
								{
									flag7 = (flag6 == m_Rx2File.RW4Section.RW4Shader_FxRenderableSimples[j].String_1.Contains("eyelashes_"));
									if (flag7)
									{
										MeshEyeLashes = new Mesh();
										MeshEyeLashes.Indices = m_Rx2File.Rx2IndexBuffers[j].IndexStream;
										MeshEyeLashes.Vertices = m_Rx2File.Rx2VertexBuffers[j].Vertexes;
									}
									else
									{
										flag7 = (flag6 == (m_Rx2File.RW4Section.RW4Shader_FxRenderableSimples[j].String_1.Contains("head_") & !m_Rx2File.RW4Section.RW4Shader_FxRenderableSimples[j].String_1.Contains("head__Copy0")));
										if (flag7)
										{
											MeshHead = new Mesh();
											MeshHead.Indices = m_Rx2File.Rx2IndexBuffers[j].IndexStream;
											MeshHead.Vertices = m_Rx2File.Rx2VertexBuffers[j].Vertexes;
										}
										else
										{
											flag7 = (flag6 == (m_Rx2File.RW4Section.RW4Shader_FxRenderableSimples[j].String_1.Contains("mouthbag_") | m_Rx2File.RW4Section.RW4Shader_FxRenderableSimples[j].String_1.Contains("head__Copy0")));
											if (flag7)
											{
												MeshMouthbag = new Mesh();
												MeshMouthbag.Indices = m_Rx2File.Rx2IndexBuffers[j].IndexStream;
												MeshMouthbag.Vertices = m_Rx2File.Rx2VertexBuffers[j].Vertexes;
											}
										}
									}
								}
							}
						}
					}
				}
			}
		}

		// Token: 0x06000292 RID: 658 RVA: 0x000380A4 File Offset: 0x000362A4
		private Mesh[] HeadsOldToNewMesh(Mesh MeshEyeLeft, Mesh MeshEyeRight, Mesh MeshEyeLashes, Mesh MeshHead, Mesh MeshMouthbag)
		{
			Mesh[] Mesh_out = new Mesh[]
			{
				new Mesh(),
				new Mesh()
			};
			checked
			{
				Mesh_out[0].Indices = new uint[MeshHead.Indices.Length + MeshMouthbag.Indices.Length - 1 + 1];
				Array.Copy(MeshHead.Indices, Mesh_out[0].Indices, MeshHead.Indices.Length);
				Array.Copy(MeshMouthbag.Indices, 0, Mesh_out[0].Indices, MeshHead.Indices.Length - 1 + 1, MeshMouthbag.Indices.Length);
				int num = MeshHead.Indices.Length - 1 + 1;
				int num2 = Mesh_out[0].Indices.Length - 1;
				for (int i = num; i <= num2; i++)
				{
					Mesh_out[0].Indices[i] = (uint)(unchecked((ulong)Mesh_out[0].Indices[i]) + (ulong)(unchecked((long)MeshHead.Vertices.Length)));
				}
				Mesh_out[1].Indices = new uint[MeshEyeLeft.Indices.Length + MeshEyeRight.Indices.Length - 1 + 1];
				Array.Copy(MeshEyeLeft.Indices, Mesh_out[1].Indices, MeshEyeLeft.Indices.Length);
				Array.Copy(MeshEyeRight.Indices, 0, Mesh_out[1].Indices, MeshEyeLeft.Indices.Length - 1 + 1, MeshEyeRight.Indices.Length);
				int num3 = MeshEyeLeft.Indices.Length - 1 + 1;
				int num4 = Mesh_out[1].Indices.Length - 1;
				for (int j = num3; j <= num4; j++)
				{
					Mesh_out[1].Indices[j] = (uint)(unchecked((ulong)Mesh_out[1].Indices[j]) + (ulong)(unchecked((long)MeshEyeLeft.Vertices.Length)));
				}
				Mesh_out[0].Vertices = new Vertex[MeshHead.Vertices.Length + MeshMouthbag.Vertices.Length - 1 + 1];
				Array.Copy(MeshHead.Vertices, Mesh_out[0].Vertices, MeshHead.Vertices.Length);
				Array.Copy(MeshMouthbag.Vertices, 0, Mesh_out[0].Vertices, MeshHead.Vertices.Length - 1 + 1, MeshMouthbag.Vertices.Length);
				Mesh_out[1].Vertices = new Vertex[MeshEyeLeft.Vertices.Length + MeshEyeRight.Vertices.Length - 1 + 1];
				Array.Copy(MeshEyeLeft.Vertices, Mesh_out[1].Vertices, MeshEyeLeft.Vertices.Length);
				Array.Copy(MeshEyeRight.Vertices, 0, Mesh_out[1].Vertices, MeshEyeLeft.Vertices.Length - 1 + 1, MeshEyeRight.Vertices.Length);
				return Mesh_out;
			}
		}

		// Token: 0x06000293 RID: 659 RVA: 0x0003831C File Offset: 0x0003651C
		private RWGObjectType_VertexDescriptor[] FixRW4VertexDescriptorsToNew(RWGObjectType_VertexDescriptor[] m_RW4VertexDescriptors)
		{
			checked
			{
				int num = m_RW4VertexDescriptors.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					int SizeChange = 0;
					int Index_delete_BiNormal = -1;
					int Index_delete_Color = -1;
					int num2 = m_RW4VertexDescriptors[b].Elements.Length - 1;
					for (int i = 0; i <= num2; i++)
					{
						m_RW4VertexDescriptors[b].Elements[i].Offset = (ushort)((int)m_RW4VertexDescriptors[b].Elements[i].Offset + SizeChange);
						bool flag = m_RW4VertexDescriptors[b].Elements[i].Usage == DeclarationUsage.TextureCoordinate & (m_RW4VertexDescriptors[b].Elements[i].DataType == D3DDECLTYPE.USHORT2N | m_RW4VertexDescriptors[b].Elements[i].DataType == D3DDECLTYPE.SHORT2N);
						if (flag)
						{
							m_RW4VertexDescriptors[b].Elements[i].DataType = D3DDECLTYPE.FLOAT16_2;
						}
						bool flag2 = m_RW4VertexDescriptors[b].Elements[i].Usage == DeclarationUsage.BiNormal & m_RW4VertexDescriptors[b].Elements[i].DataType == D3DDECLTYPE.DEC3N;
						if (flag2)
						{
							SizeChange -= 4;
							Index_delete_BiNormal = i;
						}
						bool flag3 = m_RW4VertexDescriptors[b].Elements[i].Usage == DeclarationUsage.BlendWeight & m_RW4VertexDescriptors[b].Elements[i].DataType == D3DDECLTYPE.USHORT4N;
						if (flag3)
						{
							m_RW4VertexDescriptors[b].Elements[i].DataType = D3DDECLTYPE.UBYTE4N;
							SizeChange -= 4;
						}
						bool flag4 = m_RW4VertexDescriptors[b].Elements[i].Usage == DeclarationUsage.Color & m_RW4VertexDescriptors[b].Elements[i].DataType == D3DDECLTYPE.D3DCOLOR;
						if (flag4)
						{
							SizeChange -= 4;
							bool flag5 = Index_delete_BiNormal == -1;
							if (flag5)
							{
								Index_delete_Color = i;
							}
							else
							{
								Index_delete_Color = i - 1;
							}
						}
					}
					bool flag6 = Index_delete_BiNormal != -1;
					if (flag6)
					{
						m_RW4VertexDescriptors[b].Elements = this.RemoveIndexFromArray(m_RW4VertexDescriptors[b].Elements, Index_delete_BiNormal);
						RWGObjectType_VertexDescriptor rwgobjectType_VertexDescriptor;
						(rwgobjectType_VertexDescriptor = m_RW4VertexDescriptors[b]).NumElements = rwgobjectType_VertexDescriptor.NumElements - 1;
					}
					bool flag7 = Index_delete_Color != -1;
					if (flag7)
					{
						m_RW4VertexDescriptors[b].Elements = this.RemoveIndexFromArray(m_RW4VertexDescriptors[b].Elements, Index_delete_Color);
						RWGObjectType_VertexDescriptor rwgobjectType_VertexDescriptor;
						(rwgobjectType_VertexDescriptor = m_RW4VertexDescriptors[b]).NumElements = rwgobjectType_VertexDescriptor.NumElements - 1;
					}
					m_RW4VertexDescriptors[b].VertexSize = (byte)((int)m_RW4VertexDescriptors[b].VertexSize + SizeChange);
				}
				return m_RW4VertexDescriptors;
			}
		}

		// Token: 0x06000294 RID: 660 RVA: 0x00038568 File Offset: 0x00036768
		private RWVertexElement[] RemoveIndexFromArray(RWVertexElement[] m_RWVertexElements, int m_index)
		{
			checked
			{
				RWVertexElement[] m_NewArray = new RWVertexElement[m_RWVertexElements.Length - 1 - 1 + 1];
				Array.Copy(m_RWVertexElements, 0, m_NewArray, 0, m_index + 1 - 1);
				Array.Copy(m_RWVertexElements, m_index + 1, m_NewArray, m_index, m_RWVertexElements.Length - 1 - m_index);
				return m_NewArray;
			}
		}

		// Token: 0x06000295 RID: 661 RVA: 0x000385AC File Offset: 0x000367AC
		public static List<FIFALibrary20.VertexElement[]> GetVertexElementList(int NumVertexBuffers, RWGObjectType_VertexDescriptor[] RW4VertexDescriptors)
		{
			List<FIFALibrary20.VertexElement[]> m_ListVertexElements = new List<FIFALibrary20.VertexElement[]>();
			bool flag = NumVertexBuffers == 0;
			checked
			{
				List<FIFALibrary20.VertexElement[]> GetVertexElementList;
				if (flag)
				{
					GetVertexElementList = null;
				}
				else
				{
					int num = NumVertexBuffers - 1;
					for (int v = 0; v <= num; v++)
					{
						bool flag2 = RW4VertexDescriptors.Length == 1;
						FIFALibrary20.VertexElement[] m_VertexElements;
						if (flag2)
						{
							int num2 = (int)(RW4VertexDescriptors[0].NumElements - 1);
							for (int u = 0; u <= num2; u++)
							{
								m_VertexElements = (FIFALibrary20.VertexElement[])Utils.CopyArray(m_VertexElements, new FIFALibrary20.VertexElement[(int)(RW4VertexDescriptors[0].NumElements - 1 + 1)]);
								m_VertexElements[u] = new FIFALibrary20.VertexElement
								{
									DataType = RW4VertexDescriptors[0].Elements[u].DataType,
									Usage = RW4VertexDescriptors[0].Elements[u].Usage,
									Offset = (int)RW4VertexDescriptors[0].Elements[u].Offset,
									UsageIndex = (int)RW4VertexDescriptors[0].Elements[u].UsageIndex
								};
							}
						}
						else
						{
							int num3 = (int)(RW4VertexDescriptors[v].NumElements - 1);
							for (int u2 = 0; u2 <= num3; u2++)
							{
								m_VertexElements = (FIFALibrary20.VertexElement[])Utils.CopyArray(m_VertexElements, new FIFALibrary20.VertexElement[(int)(RW4VertexDescriptors[v].NumElements - 1 + 1)]);
								m_VertexElements[u2] = new FIFALibrary20.VertexElement
								{
									DataType = RW4VertexDescriptors[v].Elements[u2].DataType,
									Usage = RW4VertexDescriptors[v].Elements[u2].Usage,
									Offset = (int)RW4VertexDescriptors[v].Elements[u2].Offset,
									UsageIndex = (int)RW4VertexDescriptors[v].Elements[u2].UsageIndex
								};
							}
						}
						m_ListVertexElements.Add(m_VertexElements);
					}
					GetVertexElementList = m_ListVertexElements;
				}
				return GetVertexElementList;
			}
		}

		// Token: 0x06000296 RID: 662 RVA: 0x00038770 File Offset: 0x00036970
		public static List<FIFALibrary20.VertexElement[]> GetVertexElementList(int NumVertexBuffers, Rx3VertexFormat[] Rx3VertexFormats)
		{
			List<FIFALibrary20.VertexElement[]> m_ListVertexElements = new List<FIFALibrary20.VertexElement[]>();
			bool flag = NumVertexBuffers == 0;
			checked
			{
				List<FIFALibrary20.VertexElement[]> GetVertexElementList;
				if (flag)
				{
					GetVertexElementList = null;
				}
				else
				{
					int num = NumVertexBuffers - 1;
					for (int v = 0; v <= num; v++)
					{
						int num2 = Rx3VertexFormats[v].Elements.Length - 1;
						FIFALibrary20.VertexElement[] m_VertexElements;
						for (int u = 0; u <= num2; u++)
						{
							m_VertexElements = (FIFALibrary20.VertexElement[])Utils.CopyArray(m_VertexElements, new FIFALibrary20.VertexElement[Rx3VertexFormats[v].Elements.Length - 1 + 1]);
							m_VertexElements[u] = new FIFALibrary20.VertexElement
							{
								DataType = Rx3VertexFormats[v].Elements[u].DataType,
								Usage = Rx3VertexFormats[v].Elements[u].Usage,
								Offset = (int)Rx3VertexFormats[v].Elements[u].Offset,
								UsageIndex = (int)Rx3VertexFormats[v].Elements[u].UsageIndex
							};
						}
						m_ListVertexElements.Add(m_VertexElements);
					}
					GetVertexElementList = m_ListVertexElements;
				}
				return GetVertexElementList;
			}
		}

		// Token: 0x06000297 RID: 663 RVA: 0x00038878 File Offset: 0x00036A78
		private bool VertexSize_IsDifferent(RWGObjectType_VertexDescriptor CompareVF1, RWGObjectType_VertexDescriptor CompareVF2)
		{
			bool flag = CompareVF1.Elements.Length != CompareVF1.Elements.Length;
			checked
			{
				bool VertexSize_IsDifferent;
				if (flag)
				{
					VertexSize_IsDifferent = true;
				}
				else
				{
					int num = CompareVF1.Elements.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = CompareVF1.Elements[i].Usage != CompareVF2.Elements[i].Usage;
						if (flag2)
						{
							return true;
						}
						bool flag3 = CompareVF1.Elements[i].Usage == CompareVF2.Elements[i].Usage;
						if (flag3)
						{
							bool flag4 = CompareVF1.Elements[i].DataType != CompareVF2.Elements[i].DataType;
							if (flag4)
							{
								bool flag5 = CompareVF1.Elements[i].Usage != DeclarationUsage.BlendIndices;
								if (flag5)
								{
									return true;
								}
							}
						}
					}
					VertexSize_IsDifferent = false;
				}
				return VertexSize_IsDifferent;
			}
		}

		// Token: 0x06000298 RID: 664 RVA: 0x0003895C File Offset: 0x00036B5C
		private bool VertexSize_IsDifferent(Rx3VertexFormat CompareVF1, RWGObjectType_VertexDescriptor CompareVF2)
		{
			bool flag = CompareVF1.Elements.Length != CompareVF1.Elements.Length;
			checked
			{
				bool VertexSize_IsDifferent;
				if (flag)
				{
					VertexSize_IsDifferent = true;
				}
				else
				{
					int num = CompareVF1.Elements.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = CompareVF1.Elements[i].Usage != CompareVF2.Elements[i].Usage;
						if (flag2)
						{
							return true;
						}
						bool flag3 = CompareVF1.Elements[i].Usage == CompareVF2.Elements[i].Usage;
						if (flag3)
						{
							bool flag4 = CompareVF1.Elements[i].DataType != CompareVF2.Elements[i].DataType;
							if (flag4)
							{
								bool flag5 = CompareVF1.Elements[i].Usage != DeclarationUsage.BlendIndices;
								if (flag5)
								{
									return true;
								}
							}
						}
					}
					VertexSize_IsDifferent = false;
				}
				return VertexSize_IsDifferent;
			}
		}

		// Token: 0x06000299 RID: 665 RVA: 0x00038A40 File Offset: 0x00036C40
		private bool VertexSize_IsDifferent(Rx3VertexFormat CompareVF1, Rx3VertexFormat CompareVF2)
		{
			bool flag = CompareVF1.Elements.Length != CompareVF1.Elements.Length;
			checked
			{
				bool VertexSize_IsDifferent;
				if (flag)
				{
					VertexSize_IsDifferent = true;
				}
				else
				{
					int num = CompareVF1.Elements.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = CompareVF1.Elements[i].Usage != CompareVF2.Elements[i].Usage;
						if (flag2)
						{
							return true;
						}
						bool flag3 = CompareVF1.Elements[i].Usage == CompareVF2.Elements[i].Usage;
						if (flag3)
						{
							bool flag4 = CompareVF1.Elements[i].DataType != CompareVF2.Elements[i].DataType;
							if (flag4)
							{
								bool flag5 = CompareVF1.Elements[i].Usage != DeclarationUsage.BlendIndices;
								if (flag5)
								{
									return true;
								}
							}
						}
					}
					VertexSize_IsDifferent = false;
				}
				return VertexSize_IsDifferent;
			}
		}

		// Token: 0x0600029A RID: 666 RVA: 0x00038B24 File Offset: 0x00036D24
		private bool VertexSize_IsDifferent(FIFALibrary20.VertexElement[] CompareVF1, FIFALibrary20.VertexElement[] CompareVF2)
		{
			bool flag = CompareVF1.Length != CompareVF1.Length;
			checked
			{
				bool VertexSize_IsDifferent;
				if (flag)
				{
					VertexSize_IsDifferent = true;
				}
				else
				{
					int num = CompareVF1.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = CompareVF1[i].Usage != CompareVF2[i].Usage;
						if (flag2)
						{
							return true;
						}
						bool flag3 = CompareVF1[i].Usage == CompareVF2[i].Usage;
						if (flag3)
						{
							bool flag4 = CompareVF1[i].DataType != CompareVF2[i].DataType;
							if (flag4)
							{
								bool flag5 = CompareVF1[i].Usage != DeclarationUsage.BlendIndices;
								if (flag5)
								{
									return true;
								}
							}
						}
					}
					VertexSize_IsDifferent = false;
				}
				return VertexSize_IsDifferent;
			}
		}

		// Token: 0x0600029B RID: 667 RVA: 0x00038BD0 File Offset: 0x00036DD0
		private Rx3VertexBuffer[] ConvertRx3VertexBuffers(Rx3VertexBuffer[] Rx3VertexBuffers_in, Rx3VertexBuffer[] Rx3VertexBuffers_out, List<FIFALibrary20.VertexElement[]> ListVertexElements_out, D3DDECLTYPE DataTypeBlendWeights, bool UpdateVFormat, bool VertexMoveScale, ref string ErrorLog)
		{
			checked
			{
				uint[] VertexSize = new uint[Rx3VertexBuffers_in.Length - 1 + 1];
				VertexEndianness[] VertexEndianness = new VertexEndianness[Rx3VertexBuffers_in.Length - 1 + 1];
				int num = Rx3VertexBuffers_in.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					long b_in = (long)(unchecked((ulong)this.Id_in[b]));
					VertexEndianness[b] = Rx3VertexBuffers_out[0].VertexEndianness;
					if (UpdateVFormat)
					{
						VertexSize[b] = Rx3VertexBuffers_in[(int)b_in].VertexSize;
					}
					else
					{
						VertexSize[b] = Rx3VertexBuffers_out[b].VertexSize;
					}
				}
				Rx3VertexBuffers_out = new Rx3VertexBuffer[Rx3VertexBuffers_in.Length - 1 + 1];
				int num2 = Rx3VertexBuffers_out.Length - 1;
				for (int b2 = 0; b2 <= num2; b2++)
				{
					long b_in;
					int NumTexcoos_ModelOut;
					int NumBlendIndices_ModelOut;
					unchecked
					{
						b_in = (long)((ulong)this.Id_in[b2]);
						NumTexcoos_ModelOut = this.GetNumTexcoosInVertex((long)b2, ListVertexElements_out);
						NumBlendIndices_ModelOut = this.GetNumBlendIndicesInVertex((long)b2, ListVertexElements_out);
						Rx3VertexBuffers_out[b2] = new Rx3VertexBuffer();
					}
					Rx3VertexBuffers_out[b2].TotalSize = Rx3VertexBuffers_in[(int)b_in].TotalSize;
					Rx3VertexBuffers_out[b2].NumVertices = Rx3VertexBuffers_in[(int)b_in].NumVertices;
					Rx3VertexBuffers_out[b2].VertexSize = VertexSize[b2];
					Rx3VertexBuffers_out[b2].VertexEndianness = VertexEndianness[b2];
					Rx3VertexBuffers_out[b2].Unknown = new byte[3];
					Rx3VertexBuffers_out[b2].Vertexes = new Vertex[(int)(unchecked((ulong)Rx3VertexBuffers_out[b2].NumVertices) - 1UL) + 1];
					long num3 = (long)(unchecked((ulong)Rx3VertexBuffers_in[checked((int)b_in)].NumVertices) - 1UL);
					for (long i = 0L; i <= num3; i += 1L)
					{
						Rx3VertexBuffers_out[b2].Vertexes[(int)i] = new Vertex
						{
							Positions = this.FixPositions(Rx3VertexBuffers_in[(int)b_in].Vertexes[(int)i].Positions, VertexMoveScale),
							TextureCoordinates = this.FixTextureCoordinates(Rx3VertexBuffers_in[(int)b_in].Vertexes[(int)i].TextureCoordinates, NumTexcoos_ModelOut, UpdateVFormat),
							Binormals = Rx3VertexBuffers_in[(int)b_in].Vertexes[(int)i].Binormals,
							Colors = Rx3VertexBuffers_in[(int)b_in].Vertexes[(int)i].Colors,
							Normals = Rx3VertexBuffers_in[(int)b_in].Vertexes[(int)i].Normals,
							Tangents = Rx3VertexBuffers_in[(int)b_in].Vertexes[(int)i].Tangents,
							BlendIndices = this.FixBlendIndices(Rx3VertexBuffers_in[(int)b_in].Vertexes[(int)i].BlendIndices, NumBlendIndices_ModelOut, UpdateVFormat, General.GetBoneSide(Rx3VertexBuffers_in[(int)b_in].Vertexes[(int)i].Positions[0].X), ref ErrorLog),
							BlendWeights = ConvertModel.FixBlendWeights(Rx3VertexBuffers_in[(int)b_in].Vertexes[(int)i].BlendWeights, NumBlendIndices_ModelOut, UpdateVFormat)
						};
						Vertex vertex;
						BlendIndices[] blendIndices = (vertex = Rx3VertexBuffers_out[b2].Vertexes[(int)i]).BlendIndices;
						Vertex vertex2;
						BlendWeights[] blendWeights = (vertex2 = Rx3VertexBuffers_out[b2].Vertexes[(int)i]).BlendWeights;
						ConvertModel.Fix_BonesSets(ref blendIndices, ref blendWeights, DataTypeBlendWeights, this.m_GameType_out, this.m_FileType);
						vertex2.BlendWeights = blendWeights;
						vertex.BlendIndices = blendIndices;
					}
				}
				return Rx3VertexBuffers_out;
			}
		}

		// Token: 0x0600029C RID: 668 RVA: 0x00038ECC File Offset: 0x000370CC
		private Rx3VertexBuffer[] ConvertRx3VertexBuffers(Rx2VertexBuffer[] Rx2VertexBuffers_in, RWGObjectType_VertexBuffer[] RW4VertexBuffer_in, Rx3VertexBuffer[] Rx3VertexBuffers_out, List<FIFALibrary20.VertexElement[]> ListVertexElements_out, D3DDECLTYPE DataTypeBlendWeights, bool UpdateVFormat, bool VertexMoveScale, ref string ErrorLog)
		{
			checked
			{
				uint[] VertexSize = new uint[Rx2VertexBuffers_in.Length - 1 + 1];
				VertexEndianness[] VertexEndianness = new VertexEndianness[Rx2VertexBuffers_in.Length - 1 + 1];
				int num = Rx2VertexBuffers_in.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					long b_in = (long)(unchecked((ulong)this.Id_in[b]));
					VertexEndianness[b] = Rx3VertexBuffers_out[0].VertexEndianness;
					if (UpdateVFormat)
					{
						VertexSize[b] = (uint)RW4VertexBuffer_in[(int)b_in].VertexSize;
					}
					else
					{
						VertexSize[b] = Rx3VertexBuffers_out[b].VertexSize;
					}
				}
				Rx3VertexBuffers_out = new Rx3VertexBuffer[Rx2VertexBuffers_in.Length - 1 + 1];
				int num2 = Rx3VertexBuffers_out.Length - 1;
				for (int b2 = 0; b2 <= num2; b2++)
				{
					long b_in;
					int NumTexcoos_ModelOut;
					int NumBlendIndices_ModelOut;
					unchecked
					{
						b_in = (long)((ulong)this.Id_in[b2]);
						NumTexcoos_ModelOut = this.GetNumTexcoosInVertex((long)b2, ListVertexElements_out);
						NumBlendIndices_ModelOut = this.GetNumBlendIndicesInVertex((long)b2, ListVertexElements_out);
						Rx3VertexBuffers_out[b2] = new Rx3VertexBuffer();
						Rx3VertexBuffers_out[b2].TotalSize = 0U;
					}
					Rx3VertexBuffers_out[b2].NumVertices = RW4VertexBuffer_in[(int)b_in].NumVertices;
					Rx3VertexBuffers_out[b2].VertexSize = VertexSize[b2];
					Rx3VertexBuffers_out[b2].VertexEndianness = VertexEndianness[b2];
					Rx3VertexBuffers_out[b2].Unknown = new byte[3];
					Rx3VertexBuffers_out[b2].Vertexes = new Vertex[(int)(unchecked((ulong)Rx3VertexBuffers_out[b2].NumVertices) - 1UL) + 1];
					long num3 = (long)(unchecked((ulong)RW4VertexBuffer_in[checked((int)b_in)].NumVertices) - 1UL);
					for (long i = 0L; i <= num3; i += 1L)
					{
						Rx3VertexBuffers_out[b2].Vertexes[(int)i] = new Vertex
						{
							Positions = this.FixPositions(Rx2VertexBuffers_in[(int)b_in].Vertexes[(int)i].Positions, VertexMoveScale),
							TextureCoordinates = this.FixTextureCoordinates(Rx2VertexBuffers_in[(int)b_in].Vertexes[(int)i].TextureCoordinates, NumTexcoos_ModelOut, UpdateVFormat),
							Binormals = Rx2VertexBuffers_in[(int)b_in].Vertexes[(int)i].Binormals,
							Colors = Rx2VertexBuffers_in[(int)b_in].Vertexes[(int)i].Colors,
							Normals = Rx2VertexBuffers_in[(int)b_in].Vertexes[(int)i].Normals,
							Tangents = Rx2VertexBuffers_in[(int)b_in].Vertexes[(int)i].Tangents,
							BlendIndices = this.FixBlendIndices(Rx2VertexBuffers_in[(int)b_in].Vertexes[(int)i].BlendIndices, NumBlendIndices_ModelOut, UpdateVFormat, General.GetBoneSide(Rx2VertexBuffers_in[(int)b_in].Vertexes[(int)i].Positions[0].X), ref ErrorLog),
							BlendWeights = ConvertModel.FixBlendWeights(Rx2VertexBuffers_in[(int)b_in].Vertexes[(int)i].BlendWeights, NumBlendIndices_ModelOut, UpdateVFormat)
						};
						Vertex vertex;
						BlendIndices[] blendIndices = (vertex = Rx3VertexBuffers_out[b2].Vertexes[(int)i]).BlendIndices;
						Vertex vertex2;
						BlendWeights[] blendWeights = (vertex2 = Rx3VertexBuffers_out[b2].Vertexes[(int)i]).BlendWeights;
						ConvertModel.Fix_BonesSets(ref blendIndices, ref blendWeights, DataTypeBlendWeights, this.m_GameType_out, this.m_FileType);
						vertex2.BlendWeights = blendWeights;
						vertex.BlendIndices = blendIndices;
					}
				}
				return Rx3VertexBuffers_out;
			}
		}

		// Token: 0x0600029D RID: 669 RVA: 0x000391C0 File Offset: 0x000373C0
		private Position[] FixPositions(Position[] Positions, bool VertexMoveScale)
		{
			return ConvertModel.FixPositions(Positions, VertexMoveScale, this.m_GameType_in, this.m_GameType_out, this.m_FileType);
		}

		// Token: 0x0600029E RID: 670 RVA: 0x000391EC File Offset: 0x000373EC
		public static Position[] FixPositions(Position[] Positions, bool VertexMoveScale, General.EGameType GameType_in, General.EGameType GameType_out, General.EFileType FileType)
		{
			bool flag = Positions == null;
			checked
			{
				Position[] FixPositions;
				if (flag)
				{
					FixPositions = null;
				}
				else
				{
					int num = Positions.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						if (VertexMoveScale)
						{
							Positions[i] = VertexMovements.MoveScale(Positions[i], FileType, GameType_in, GameType_out);
						}
						bool flag2 = General.IsGameOldEngine(GameType_out) & !General.IsGameOldEngine(GameType_in);
						if (flag2)
						{
							Positions[i].W = 1f;
						}
					}
					FixPositions = Positions;
				}
				return FixPositions;
			}
		}

		// Token: 0x0600029F RID: 671 RVA: 0x0003925C File Offset: 0x0003745C
		private TextureCoordinate[] FixTextureCoordinates(TextureCoordinate[] TextureCoordinates_In, int NumTexcoos_ModelOut, bool UpdateVFormat)
		{
			bool flag = TextureCoordinates_In == null;
			checked
			{
				TextureCoordinate[] FixTextureCoordinates;
				if (flag)
				{
					FixTextureCoordinates = null;
				}
				else
				{
					int NumTexcoos_ModelIn = TextureCoordinates_In.Length;
					bool flag2 = !UpdateVFormat & NumTexcoos_ModelOut > NumTexcoos_ModelIn;
					if (flag2)
					{
						TextureCoordinate[] TextureCoordinates_Return = new TextureCoordinate[NumTexcoos_ModelOut - 1 + 1];
						int num = NumTexcoos_ModelOut - 1;
						for (int i = 0; i <= num; i++)
						{
							bool flag3 = i <= NumTexcoos_ModelIn - 1;
							if (flag3)
							{
								TextureCoordinates_Return[i] = TextureCoordinates_In[i];
							}
							else
							{
								TextureCoordinates_Return[i] = TextureCoordinates_In[NumTexcoos_ModelIn - 1];
							}
						}
						FixTextureCoordinates = TextureCoordinates_Return;
					}
					else
					{
						FixTextureCoordinates = TextureCoordinates_In;
					}
				}
				return FixTextureCoordinates;
			}
		}

		// Token: 0x060002A0 RID: 672 RVA: 0x000392DC File Offset: 0x000374DC
		private BlendIndices[] FixBlendIndices(BlendIndices[] BlendIndices_In, int NumBlendIndices_ModelOut, bool UpdateVFormat, General.EBoneSide BoneSide, ref string ErrorLog)
		{
			return ConvertModel.FixBlendIndices(BlendIndices_In, NumBlendIndices_ModelOut, UpdateVFormat, BoneSide, this.m_ConvertBones, ref ErrorLog);
		}

		// Token: 0x060002A1 RID: 673 RVA: 0x00039300 File Offset: 0x00037500
		public static BlendIndices[] FixBlendIndices(BlendIndices[] BlendIndices_In, int NumBlendIndices_ModelOut, bool UpdateVFormat, General.EBoneSide BoneSide, ConvertBones BonesConvert, ref string ErrorLog)
		{
			bool flag = BlendIndices_In == null;
			checked
			{
				BlendIndices[] FixBlendIndices;
				if (flag)
				{
					FixBlendIndices = null;
				}
				else
				{
					int NumBlendIndices_ModelIn = BlendIndices_In.Length;
					BlendIndices[] BlendIndices_Out = new BlendIndices[NumBlendIndices_ModelIn - 1 + 1];
					int num = BlendIndices_Out.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = i <= NumBlendIndices_ModelIn - 1;
						if (flag2)
						{
							BlendIndices_Out[i] = new BlendIndices
							{
								Index_1 = BonesConvert.ConvertBoneIndex((short)BlendIndices_In[i].Index_1, BoneSide, true, ref ErrorLog),
								Index_2 = BonesConvert.ConvertBoneIndex((short)BlendIndices_In[i].Index_2, BoneSide, true, ref ErrorLog),
								Index_3 = BonesConvert.ConvertBoneIndex((short)BlendIndices_In[i].Index_3, BoneSide, true, ref ErrorLog),
								Index_4 = BonesConvert.ConvertBoneIndex((short)BlendIndices_In[i].Index_4, BoneSide, true, ref ErrorLog)
							};
						}
						else
						{
							BlendIndices_Out[i] = new BlendIndices
							{
								Index_1 = 0,
								Index_2 = 0,
								Index_3 = 0,
								Index_4 = 0
							};
						}
					}
					FixBlendIndices = BlendIndices_Out;
				}
				return FixBlendIndices;
			}
		}

		// Token: 0x060002A2 RID: 674 RVA: 0x00039414 File Offset: 0x00037614
		public static BlendWeights[] FixBlendWeights(BlendWeights[] BlendWeights_In, int NumBlendWeights_ModelOut, bool UpdateVFormat)
		{
			bool flag = BlendWeights_In == null;
			checked
			{
				BlendWeights[] FixBlendWeights;
				if (flag)
				{
					FixBlendWeights = null;
				}
				else
				{
					int NumBlendWeights_ModelIn = BlendWeights_In.Length;
					BlendWeights[] BlendWeights_Out = new BlendWeights[NumBlendWeights_ModelIn - 1 + 1];
					int num = BlendWeights_Out.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = i <= NumBlendWeights_ModelIn - 1;
						if (flag2)
						{
							BlendWeights_Out[i] = BlendWeights_In[i];
						}
						else
						{
							BlendWeights_Out[i] = new BlendWeights
							{
								Weight_1 = 0f,
								Weight_2 = 0f,
								Weight_3 = 0f,
								Weight_4 = 0f
							};
						}
					}
					FixBlendWeights = BlendWeights_Out;
				}
				return FixBlendWeights;
			}
		}

		// Token: 0x060002A3 RID: 675 RVA: 0x000394B4 File Offset: 0x000376B4
		public static void Fix_BonesSets(ref BlendIndices[] m_BlendIndices, ref BlendWeights[] m_BlendWeights, D3DDECLTYPE DataTypeBlendWeights, General.EGameType GameType, General.EFileType FileType)
		{
			bool flag = !(m_BlendIndices == null | m_BlendWeights == null);
			checked
			{
				if (flag)
				{
					int NumBonesSets_Current = m_BlendIndices.Length;
					bool flag2 = FileType == General.EFileType.HEAD_MODEL;
					int NumBonesSets_New;
					if (flag2)
					{
						bool flag3 = GameType == General.EGameType.FIFA_15 | GameType == General.EGameType.FIFA_16 | General.IsGameFrostbiteEngine(GameType);
						if (flag3)
						{
							NumBonesSets_New = 2;
						}
						else
						{
							NumBonesSets_New = 1;
						}
					}
					else
					{
						NumBonesSets_New = NumBonesSets_Current;
					}
					Bones[] BonesArray = ConvertModel.GetBonesArray(m_BlendIndices, m_BlendWeights);
					ConvertModel.MergeSimilarBones(ref BonesArray, DataTypeBlendWeights);
					BonesArray = BonesArray.OrderByDescending((ConvertModel._Closure$__.$I24-0 == null) ? (ConvertModel._Closure$__.$I24-0 = ((Bones c) => c.BlendWeight)) : ConvertModel._Closure$__.$I24-0).ToArray<Bones>();
					BonesArray = ConvertModel.FixUnusedBones(ref BonesArray);
					ConvertModel.SetBonesArray(BonesArray, ref m_BlendIndices, ref m_BlendWeights);
					bool flag4 = NumBonesSets_Current == 2 & NumBonesSets_New == 1;
					if (flag4)
					{
						unchecked
						{
							switch (3)
							{
							case 1:
								m_BlendWeights[0].Weight_1 = (float)((Math.Round((double)(m_BlendWeights[0].Weight_1 * 255f), 0) + Math.Round((double)(m_BlendWeights[1].Weight_1 * 255f), 0)) / 255.0);
								m_BlendWeights[0].Weight_2 = (float)((Math.Round((double)(m_BlendWeights[0].Weight_2 * 255f), 0) + Math.Round((double)(m_BlendWeights[1].Weight_2 * 255f), 0)) / 255.0);
								m_BlendWeights[0].Weight_3 = (float)((Math.Round((double)(m_BlendWeights[0].Weight_3 * 255f), 0) + Math.Round((double)(m_BlendWeights[1].Weight_3 * 255f), 0)) / 255.0);
								m_BlendWeights[0].Weight_4 = (float)((Math.Round((double)(m_BlendWeights[0].Weight_4 * 255f), 0) + Math.Round((double)(m_BlendWeights[1].Weight_4 * 255f), 0)) / 255.0);
								break;
							case 2:
								m_BlendWeights[0].Weight_1 = (float)((Math.Round((double)(m_BlendWeights[0].Weight_1 * 255f), 0) + Math.Round((double)(m_BlendWeights[1].Weight_4 * 255f), 0)) / 255.0);
								m_BlendWeights[0].Weight_2 = (float)((Math.Round((double)(m_BlendWeights[0].Weight_2 * 255f), 0) + Math.Round((double)(m_BlendWeights[1].Weight_3 * 255f), 0)) / 255.0);
								m_BlendWeights[0].Weight_3 = (float)((Math.Round((double)(m_BlendWeights[0].Weight_3 * 255f), 0) + Math.Round((double)(m_BlendWeights[1].Weight_2 * 255f), 0)) / 255.0);
								m_BlendWeights[0].Weight_4 = (float)((Math.Round((double)(m_BlendWeights[0].Weight_4 * 255f), 0) + Math.Round((double)(m_BlendWeights[1].Weight_1 * 255f), 0)) / 255.0);
								break;
							case 3:
								m_BlendWeights[0] = ConvertModel.NormalizeBlendWeights(m_BlendWeights[0], DataTypeBlendWeights);
								break;
							}
						}
						m_BlendIndices = (BlendIndices[])Utils.CopyArray(m_BlendIndices, new BlendIndices[NumBonesSets_New - 1 + 1]);
						m_BlendWeights = (BlendWeights[])Utils.CopyArray(m_BlendWeights, new BlendWeights[NumBonesSets_New - 1 + 1]);
					}
					else
					{
						bool flag5 = NumBonesSets_Current == 1 & NumBonesSets_New == 2;
						if (flag5)
						{
							m_BlendIndices = (BlendIndices[])Utils.CopyArray(m_BlendIndices, new BlendIndices[NumBonesSets_New - 1 + 1]);
							m_BlendWeights = (BlendWeights[])Utils.CopyArray(m_BlendWeights, new BlendWeights[NumBonesSets_New - 1 + 1]);
							int num = NumBonesSets_Current - 1 + 1;
							int num2 = NumBonesSets_New - 1;
							for (int i = num; i <= num2; i++)
							{
								m_BlendIndices[i] = new BlendIndices
								{
									Index_1 = m_BlendIndices[0].Index_4,
									Index_2 = m_BlendIndices[0].Index_4,
									Index_3 = m_BlendIndices[0].Index_4,
									Index_4 = m_BlendIndices[0].Index_4
								};
								m_BlendWeights[i] = new BlendWeights
								{
									Weight_1 = 0f,
									Weight_2 = 0f,
									Weight_3 = 0f,
									Weight_4 = 0f
								};
							}
							m_BlendWeights[0] = ConvertModel.NormalizeBlendWeights(m_BlendWeights[0], DataTypeBlendWeights);
						}
						else
						{
							bool flag6 = NumBonesSets_Current == 1 & NumBonesSets_New == 1;
							if (flag6)
							{
								m_BlendWeights[0] = ConvertModel.NormalizeBlendWeights(m_BlendWeights[0], DataTypeBlendWeights);
							}
						}
					}
				}
			}
		}

		// Token: 0x060002A4 RID: 676 RVA: 0x00039914 File Offset: 0x00037B14
		private static ushort[] GetArrayFromBlendIndices(BlendIndices[] m_BlendIndices)
		{
			checked
			{
				ushort[] ReturnBlendIndices = new ushort[m_BlendIndices.Length * 4 - 1 + 1];
				int index = 0;
				int num = m_BlendIndices.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					ReturnBlendIndices[index] = m_BlendIndices[i].Index_1;
					index++;
					ReturnBlendIndices[index] = m_BlendIndices[i].Index_2;
					index++;
					ReturnBlendIndices[index] = m_BlendIndices[i].Index_3;
					index++;
					ReturnBlendIndices[index] = m_BlendIndices[i].Index_4;
					index++;
				}
				return ReturnBlendIndices;
			}
		}

		// Token: 0x060002A5 RID: 677 RVA: 0x00039990 File Offset: 0x00037B90
		private static float[] GetArrayFromBlendWeights(BlendWeights[] m_BlendWeights)
		{
			checked
			{
				float[] ReturnBlendWeights = new float[m_BlendWeights.Length * 4 - 1 + 1];
				int index = 0;
				int num = m_BlendWeights.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					ReturnBlendWeights[index] = m_BlendWeights[i].Weight_1;
					index++;
					ReturnBlendWeights[index] = m_BlendWeights[i].Weight_2;
					index++;
					ReturnBlendWeights[index] = m_BlendWeights[i].Weight_3;
					index++;
					ReturnBlendWeights[index] = m_BlendWeights[i].Weight_4;
					index++;
				}
				return ReturnBlendWeights;
			}
		}

		// Token: 0x060002A6 RID: 678 RVA: 0x00039A0C File Offset: 0x00037C0C
		private static Bones[] GetBonesArray(BlendIndices[] m_BlendIndices, BlendWeights[] m_BlendWeights)
		{
			checked
			{
				Bones[] ReturnBonesArray = new Bones[m_BlendIndices.Length * 4 - 1 + 1];
				int index = 0;
				int num = m_BlendIndices.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					ReturnBonesArray[index] = new Bones();
					ReturnBonesArray[index].BlendIndex = m_BlendIndices[i].Index_1;
					ReturnBonesArray[index].BlendWeight = m_BlendWeights[i].Weight_1;
					index++;
					ReturnBonesArray[index] = new Bones();
					ReturnBonesArray[index].BlendIndex = m_BlendIndices[i].Index_2;
					ReturnBonesArray[index].BlendWeight = m_BlendWeights[i].Weight_2;
					index++;
					ReturnBonesArray[index] = new Bones();
					ReturnBonesArray[index].BlendIndex = m_BlendIndices[i].Index_3;
					ReturnBonesArray[index].BlendWeight = m_BlendWeights[i].Weight_3;
					index++;
					ReturnBonesArray[index] = new Bones();
					ReturnBonesArray[index].BlendIndex = m_BlendIndices[i].Index_4;
					ReturnBonesArray[index].BlendWeight = m_BlendWeights[i].Weight_4;
					index++;
				}
				return ReturnBonesArray;
			}
		}

		// Token: 0x060002A7 RID: 679 RVA: 0x00039B0C File Offset: 0x00037D0C
		private static void SetBonesArray(Bones[] BonesArray, ref BlendIndices[] m_BlendIndices, ref BlendWeights[] m_BlendWeights)
		{
			checked
			{
				m_BlendIndices = new BlendIndices[BonesArray.Length / 4 - 1 + 1];
				m_BlendWeights = new BlendWeights[BonesArray.Length / 4 - 1 + 1];
				int index = 0;
				int num = m_BlendIndices.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					m_BlendIndices[i] = new BlendIndices();
					m_BlendWeights[i] = new BlendWeights();
					m_BlendIndices[i].Index_1 = BonesArray[index].BlendIndex;
					m_BlendWeights[i].Weight_1 = BonesArray[index].BlendWeight;
					index++;
					m_BlendIndices[i].Index_2 = BonesArray[index].BlendIndex;
					m_BlendWeights[i].Weight_2 = BonesArray[index].BlendWeight;
					index++;
					m_BlendIndices[i].Index_3 = BonesArray[index].BlendIndex;
					m_BlendWeights[i].Weight_3 = BonesArray[index].BlendWeight;
					index++;
					m_BlendIndices[i].Index_4 = BonesArray[index].BlendIndex;
					m_BlendWeights[i].Weight_4 = BonesArray[index].BlendWeight;
					index++;
				}
			}
		}

		// Token: 0x060002A8 RID: 680 RVA: 0x00039C08 File Offset: 0x00037E08
		private static void MergeSimilarBones(ref Bones[] BonesArray, D3DDECLTYPE DataType)
		{
			int Value_devide = 255;
			if (DataType != D3DDECLTYPE.USHORT4N)
			{
				if (DataType == D3DDECLTYPE.UBYTE4N)
				{
					Value_devide = 255;
				}
			}
			else
			{
				Value_devide = 65535;
			}
			checked
			{
				int num = BonesArray.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = i < BonesArray.Length - 1;
					if (flag)
					{
						long SameBone = ConvertModel.SearchNextBoneIndex(BonesArray, BonesArray[i].BlendIndex, unchecked((long)(checked(i + 1))));
						bool flag2 = SameBone != -1L && BonesArray[(int)SameBone].BlendWeight != 0f;
						if (flag2)
						{
							BonesArray[(int)SameBone].BlendIndex = 0;
							BonesArray[i].BlendWeight = (float)(unchecked(Math.Round((double)(BonesArray[i].BlendWeight * (float)Value_devide), 0) + Math.Round((double)(BonesArray[checked((int)SameBone)].BlendWeight * (float)Value_devide), 0)));
							BonesArray[i].BlendWeight = BonesArray[i].BlendWeight / (float)Value_devide;
							BonesArray[(int)SameBone].BlendWeight = 0f;
						}
					}
				}
			}
		}

		// Token: 0x060002A9 RID: 681 RVA: 0x00039D18 File Offset: 0x00037F18
		private static long SearchNextBoneIndex(Bones[] BonesArray, ushort FindBoneIndex, long SearchStartIndex)
		{
			bool flag = SearchStartIndex > (long)(checked(BonesArray.Length - 1));
			long SearchNextBoneIndex;
			if (flag)
			{
				SearchNextBoneIndex = -1L;
			}
			else
			{
				long num = (long)(checked(BonesArray.Length - 1));
				checked
				{
					for (long i = SearchStartIndex; i <= num; i += 1L)
					{
						bool flag2 = BonesArray[(int)i].BlendIndex == FindBoneIndex;
						if (flag2)
						{
							return i;
						}
					}
					SearchNextBoneIndex = -1L;
				}
			}
			return SearchNextBoneIndex;
		}

		// Token: 0x060002AA RID: 682 RVA: 0x00039D74 File Offset: 0x00037F74
		private static Bones[] FixUnusedBones(ref Bones[] BonesArray)
		{
			checked
			{
				int num = BonesArray.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = BonesArray[i].BlendWeight == 0f & i > 0;
					if (flag)
					{
						BonesArray[i].BlendIndex = BonesArray[i - 1].BlendIndex;
					}
				}
				return BonesArray;
			}
		}

		// Token: 0x060002AB RID: 683 RVA: 0x00039DCC File Offset: 0x00037FCC
		private static BlendWeights NormalizeBlendWeights(BlendWeights m_BlendWeights, D3DDECLTYPE DataType)
		{
			int Value_devide = 255;
			if (DataType != D3DDECLTYPE.USHORT4N)
			{
				if (DataType == D3DDECLTYPE.UBYTE4N)
				{
					Value_devide = 255;
				}
			}
			else
			{
				Value_devide = 65535;
			}
			int Value_normalize_needed = checked((int)Math.Round(unchecked((double)Value_devide - (Math.Round((double)(m_BlendWeights.Weight_4 * (float)Value_devide), 0) + Math.Round((double)(m_BlendWeights.Weight_3 * (float)Value_devide), 0) + Math.Round((double)(m_BlendWeights.Weight_2 * (float)Value_devide), 0) + Math.Round((double)(m_BlendWeights.Weight_1 * (float)Value_devide), 0)))));
			bool flag = Value_normalize_needed != 0;
			if (flag)
			{
				int NumValues = 0;
				bool flag2 = m_BlendWeights.Weight_4 != 0f;
				int Value_multiply;
				int Value_rest;
				bool flag6;
				checked
				{
					if (flag2)
					{
						NumValues++;
					}
					bool flag3 = m_BlendWeights.Weight_3 != 0f;
					if (flag3)
					{
						NumValues++;
					}
					bool flag4 = m_BlendWeights.Weight_2 != 0f;
					if (flag4)
					{
						NumValues++;
					}
					bool flag5 = m_BlendWeights.Weight_1 != 0f;
					if (flag5)
					{
						NumValues++;
					}
					Value_multiply = Value_normalize_needed / NumValues;
					Value_rest = Value_normalize_needed - Value_multiply * NumValues;
					flag6 = (m_BlendWeights.Weight_1 != 0f);
				}
				if (flag6)
				{
					m_BlendWeights.Weight_1 = (float)(Math.Round((double)(m_BlendWeights.Weight_1 * (float)Value_devide), 0) + (double)Value_multiply);
					bool flag7 = Value_rest != 0;
					if (flag7)
					{
						bool flag8 = Value_rest < 0;
						if (flag8)
						{
							m_BlendWeights.Weight_1 -= 1f;
							checked
							{
								Value_rest++;
							}
						}
						else
						{
							bool flag9 = Value_rest > 0;
							if (flag9)
							{
								m_BlendWeights.Weight_1 += 1f;
								checked
								{
									Value_rest--;
								}
							}
						}
					}
					m_BlendWeights.Weight_1 /= (float)Value_devide;
				}
				bool flag10 = m_BlendWeights.Weight_2 != 0f;
				if (flag10)
				{
					m_BlendWeights.Weight_2 = (float)(Math.Round((double)(m_BlendWeights.Weight_2 * (float)Value_devide), 0) + (double)Value_multiply);
					bool flag11 = Value_rest != 0;
					if (flag11)
					{
						bool flag12 = Value_rest < 0;
						if (flag12)
						{
							m_BlendWeights.Weight_2 -= 1f;
							checked
							{
								Value_rest++;
							}
						}
						else
						{
							bool flag13 = Value_rest > 0;
							if (flag13)
							{
								m_BlendWeights.Weight_2 += 1f;
								checked
								{
									Value_rest--;
								}
							}
						}
					}
					m_BlendWeights.Weight_2 /= (float)Value_devide;
				}
				bool flag14 = m_BlendWeights.Weight_3 != 0f;
				if (flag14)
				{
					m_BlendWeights.Weight_3 = (float)(Math.Round((double)(m_BlendWeights.Weight_3 * (float)Value_devide), 0) + (double)Value_multiply);
					bool flag15 = Value_rest != 0;
					if (flag15)
					{
						bool flag16 = Value_rest < 0;
						if (flag16)
						{
							m_BlendWeights.Weight_3 -= 1f;
							checked
							{
								Value_rest++;
							}
						}
						else
						{
							bool flag17 = Value_rest > 0;
							if (flag17)
							{
								m_BlendWeights.Weight_3 += 1f;
								checked
								{
									Value_rest--;
								}
							}
						}
					}
					m_BlendWeights.Weight_3 /= (float)Value_devide;
				}
				bool flag18 = m_BlendWeights.Weight_4 != 0f;
				if (flag18)
				{
					m_BlendWeights.Weight_4 = (float)(Math.Round((double)(m_BlendWeights.Weight_4 * (float)Value_devide), 0) + (double)Value_multiply);
					bool flag19 = Value_rest != 0;
					if (flag19)
					{
						bool flag20 = Value_rest < 0;
						if (flag20)
						{
							m_BlendWeights.Weight_4 -= 1f;
							checked
							{
								Value_rest++;
							}
						}
						else
						{
							bool flag21 = Value_rest > 0;
							if (flag21)
							{
								m_BlendWeights.Weight_4 += 1f;
								checked
								{
									Value_rest--;
								}
							}
						}
					}
					m_BlendWeights.Weight_4 /= (float)Value_devide;
				}
				bool flag22 = Math.Round((double)(m_BlendWeights.Weight_4 * (float)Value_devide), 0) + Math.Round((double)(m_BlendWeights.Weight_3 * (float)Value_devide), 0) + Math.Round((double)(m_BlendWeights.Weight_2 * (float)Value_devide), 0) + Math.Round((double)(m_BlendWeights.Weight_1 * (float)Value_devide), 0) != (double)Value_devide;
				if (flag22)
				{
					Interaction.MsgBox(Math.Round((double)(m_BlendWeights.Weight_4 * (float)Value_devide), 0) + Math.Round((double)(m_BlendWeights.Weight_3 * (float)Value_devide), 0) + Math.Round((double)(m_BlendWeights.Weight_2 * (float)Value_devide), 0) + Math.Round((double)(m_BlendWeights.Weight_1 * (float)Value_devide), 0), MsgBoxStyle.OkOnly, null);
				}
			}
			return m_BlendWeights;
		}

		// Token: 0x060002AC RID: 684 RVA: 0x0003A230 File Offset: 0x00038430
		private long GetInputId_fromNameTable(long Id_Buffer_out, NameTable[] NameTable_in, NameTable[] NameTable_out)
		{
			string StrName_out = "";
			uint ObjectId_out = 0U;
			bool flag = Id_Buffer_out <= (long)(checked(NameTable_out.Length - 1));
			checked
			{
				if (flag)
				{
					StrName_out = NameTable_out[(int)Id_Buffer_out].Name;
					ObjectId_out = NameTable_out[(int)Id_Buffer_out].ObjectId;
				}
				General.EFileType fileType = this.m_FileType;
				if (fileType == General.EFileType.HEAD_MODEL)
				{
					bool flag2 = NameTable_in.Length != NameTable_out.Length;
					if (flag2)
					{
						return Id_Buffer_out;
					}
					bool flag3 = StrName_out.Contains("eyes") & (ObjectId_out == 3566041216U | ObjectId_out == 15663108U);
					if (flag3)
					{
						int num = NameTable_out.Length - 1;
						for (int b = 0; b <= num; b++)
						{
							bool flag4 = NameTable_in[b].Name.Contains("eyes") & (NameTable_in[b].ObjectId == 3566041216U | NameTable_in[b].ObjectId == 15663108U);
							if (flag4)
							{
								return unchecked((long)b);
							}
						}
					}
					else
					{
						bool flag5 = StrName_out.Contains("head") & (ObjectId_out == 3566041216U | ObjectId_out == 15663108U) & !StrName_out.Contains("eyes");
						if (flag5)
						{
							int num2 = NameTable_out.Length - 1;
							for (int b2 = 0; b2 <= num2; b2++)
							{
								bool flag6 = NameTable_in[b2].Name.Contains("head") & !NameTable_in[b2].Name.Contains("eyes") & (NameTable_in[b2].ObjectId == 3566041216U | NameTable_in[b2].ObjectId == 15663108U);
								if (flag6)
								{
									return unchecked((long)b2);
								}
							}
						}
					}
				}
				return Id_Buffer_out;
			}
		}

		// Token: 0x060002AD RID: 685 RVA: 0x0003A3CC File Offset: 0x000385CC
		private int GetNumBlendIndicesInVertex(long IdVertexBuffer, List<FIFALibrary20.VertexElement[]> ListVertexElements)
		{
			bool flag = (long)(checked(ListVertexElements.Count - 1)) < IdVertexBuffer;
			if (flag)
			{
				IdVertexBuffer = 0L;
			}
			return this.NumBlendIndicesInVertex(ListVertexElements[checked((int)IdVertexBuffer)]);
		}

		// Token: 0x060002AE RID: 686 RVA: 0x0003A404 File Offset: 0x00038604
		private int GetNumBlendIndicesInVertex(long IdVertexBuffer, RWGObjectType_VertexDescriptor[] RW4VertexDescriptors)
		{
			bool flag = (long)(checked(RW4VertexDescriptors.Length - 1)) < IdVertexBuffer;
			if (flag)
			{
				IdVertexBuffer = 0L;
			}
			return this.NumBlendIndicesInVertex(RW4VertexDescriptors[checked((int)IdVertexBuffer)]);
		}

		// Token: 0x060002AF RID: 687 RVA: 0x0003A434 File Offset: 0x00038634
		private int GetNumBlendIndicesInVertex(long IdVertexBuffer, Rx3VertexFormat[] Rx3VertexFormats)
		{
			bool flag = (long)(checked(Rx3VertexFormats.Length - 1)) < IdVertexBuffer;
			if (flag)
			{
				IdVertexBuffer = 0L;
			}
			return this.NumBlendIndicesInVertex(Rx3VertexFormats[checked((int)IdVertexBuffer)]);
		}

		// Token: 0x060002B0 RID: 688 RVA: 0x0003A464 File Offset: 0x00038664
		private int NumBlendIndicesInVertex(FIFALibrary20.VertexElement[] VertexElements)
		{
			int ReturnValue = 0;
			checked
			{
				int num = VertexElements.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = VertexElements[i].Usage == DeclarationUsage.BlendIndices;
					if (flag)
					{
						ReturnValue++;
					}
				}
				return ReturnValue;
			}
		}

		// Token: 0x060002B1 RID: 689 RVA: 0x0003A4A4 File Offset: 0x000386A4
		private int NumBlendIndicesInVertex(RWGObjectType_VertexDescriptor VertexDescriptor)
		{
			int ReturnValue = 0;
			checked
			{
				int num = (int)(VertexDescriptor.NumElements - 1);
				for (int i = 0; i <= num; i++)
				{
					bool flag = VertexDescriptor.Elements[i].Usage == DeclarationUsage.BlendIndices;
					if (flag)
					{
						ReturnValue++;
					}
				}
				return ReturnValue;
			}
		}

		// Token: 0x060002B2 RID: 690 RVA: 0x0003A4EC File Offset: 0x000386EC
		private int NumBlendIndicesInVertex(Rx3VertexFormat m_VertexFormat)
		{
			int ReturnValue = 0;
			checked
			{
				int num = m_VertexFormat.Elements.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = m_VertexFormat.Elements[i].Usage == DeclarationUsage.BlendIndices;
					if (flag)
					{
						ReturnValue++;
					}
				}
				return ReturnValue;
			}
		}

		// Token: 0x060002B3 RID: 691 RVA: 0x0003A534 File Offset: 0x00038734
		private int GetNumTexcoosInVertex(long IdVertexBuffer, List<FIFALibrary20.VertexElement[]> ListVertexElements)
		{
			bool flag = (long)(checked(ListVertexElements.Count - 1)) < IdVertexBuffer;
			if (flag)
			{
				IdVertexBuffer = 0L;
			}
			return ConvertModel.NumTexcoosInVertex(ListVertexElements[checked((int)IdVertexBuffer)]);
		}

		// Token: 0x060002B4 RID: 692 RVA: 0x0003A56C File Offset: 0x0003876C
		private int GetNumTexcoosInVertex(long IdVertexBuffer, RWGObjectType_VertexDescriptor[] RW4VertexDescriptors)
		{
			bool flag = (long)(checked(RW4VertexDescriptors.Length - 1)) < IdVertexBuffer;
			if (flag)
			{
				IdVertexBuffer = 0L;
			}
			return this.NumTexcoosInVertex(RW4VertexDescriptors[checked((int)IdVertexBuffer)]);
		}

		// Token: 0x060002B5 RID: 693 RVA: 0x0003A59C File Offset: 0x0003879C
		private int GetNumTexcoosInVertex(long IdVertexBuffer, Rx3VertexFormat[] Rx3VertexFormats)
		{
			bool flag = (long)(checked(Rx3VertexFormats.Length - 1)) < IdVertexBuffer;
			if (flag)
			{
				IdVertexBuffer = 0L;
			}
			return ConvertModel.NumTexcoosInVertex(Rx3VertexFormats[checked((int)IdVertexBuffer)]);
		}

		// Token: 0x060002B6 RID: 694 RVA: 0x0003A5CC File Offset: 0x000387CC
		public static int NumTexcoosInVertex(FIFALibrary20.VertexElement[] ListVertexElements)
		{
			int ReturnValue = 0;
			checked
			{
				int num = ListVertexElements.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = ListVertexElements[i].Usage == DeclarationUsage.TextureCoordinate;
					if (flag)
					{
						ReturnValue++;
					}
				}
				return ReturnValue;
			}
		}

		// Token: 0x060002B7 RID: 695 RVA: 0x0003A60C File Offset: 0x0003880C
		private int NumTexcoosInVertex(RWGObjectType_VertexDescriptor m_RW4VertexDescriptor)
		{
			int ReturnValue = 0;
			checked
			{
				int num = (int)(m_RW4VertexDescriptor.NumElements - 1);
				for (int i = 0; i <= num; i++)
				{
					bool flag = m_RW4VertexDescriptor.Elements[i].Usage == DeclarationUsage.TextureCoordinate;
					if (flag)
					{
						ReturnValue++;
					}
				}
				return ReturnValue;
			}
		}

		// Token: 0x060002B8 RID: 696 RVA: 0x0003A654 File Offset: 0x00038854
		public static int NumTexcoosInVertex(Rx3VertexFormat m_VertexFormat)
		{
			int ReturnValue = 0;
			checked
			{
				int num = m_VertexFormat.Elements.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = m_VertexFormat.Elements[i].Usage == DeclarationUsage.TextureCoordinate;
					if (flag)
					{
						ReturnValue++;
					}
				}
				return ReturnValue;
			}
		}

		// Token: 0x060002B9 RID: 697 RVA: 0x0003A69C File Offset: 0x0003889C
		private BlendIndices RemoveEmptyBlendindices(BlendIndices m_BlendIndices_out, BlendIndices m_BlendIndices_in, General.EBoneSide BoneSide, ref string ErrorLog)
		{
			bool flag = m_BlendIndices_out.Index_1 == 0;
			if (flag)
			{
				bool flag2 = m_BlendIndices_out.Index_2 > 0;
				if (flag2)
				{
					m_BlendIndices_out.Index_1 = m_BlendIndices_out.Index_2;
				}
				else
				{
					bool flag3 = m_BlendIndices_out.Index_3 > 0;
					if (flag3)
					{
						m_BlendIndices_out.Index_1 = m_BlendIndices_out.Index_3;
					}
					else
					{
						m_BlendIndices_out.Index_1 = m_BlendIndices_out.Index_4;
					}
				}
			}
			bool flag4 = m_BlendIndices_out.Index_2 == 0;
			if (flag4)
			{
				bool flag5 = m_BlendIndices_out.Index_1 > 0;
				if (flag5)
				{
					m_BlendIndices_out.Index_2 = m_BlendIndices_out.Index_1;
				}
				else
				{
					bool flag6 = m_BlendIndices_out.Index_3 > 0;
					if (flag6)
					{
						m_BlendIndices_out.Index_2 = m_BlendIndices_out.Index_3;
					}
					else
					{
						m_BlendIndices_out.Index_2 = m_BlendIndices_out.Index_4;
					}
				}
			}
			bool flag7 = m_BlendIndices_out.Index_3 == 0;
			if (flag7)
			{
				bool flag8 = m_BlendIndices_out.Index_2 > 0;
				if (flag8)
				{
					m_BlendIndices_out.Index_3 = m_BlendIndices_out.Index_2;
				}
				else
				{
					bool flag9 = m_BlendIndices_out.Index_1 > 0;
					if (flag9)
					{
						m_BlendIndices_out.Index_3 = m_BlendIndices_out.Index_1;
					}
					else
					{
						m_BlendIndices_out.Index_3 = m_BlendIndices_out.Index_4;
					}
				}
			}
			bool flag10 = m_BlendIndices_out.Index_4 == 0;
			if (flag10)
			{
				bool flag11 = m_BlendIndices_out.Index_3 > 0;
				if (flag11)
				{
					m_BlendIndices_out.Index_4 = m_BlendIndices_out.Index_3;
				}
				else
				{
					bool flag12 = m_BlendIndices_out.Index_2 > 0;
					if (flag12)
					{
						m_BlendIndices_out.Index_4 = m_BlendIndices_out.Index_2;
					}
					else
					{
						m_BlendIndices_out.Index_4 = m_BlendIndices_out.Index_1;
					}
				}
			}
			bool flag13 = m_BlendIndices_out.Index_1 == 0 & m_BlendIndices_out.Index_2 == 0 & m_BlendIndices_out.Index_3 == 0 & m_BlendIndices_out.Index_4 == 0;
			checked
			{
				if (flag13)
				{
					m_BlendIndices_out.Index_1 = this.m_ConvertBones.ConvertBoneIndex((short)m_BlendIndices_in.Index_1, BoneSide, true, ref ErrorLog);
					m_BlendIndices_out.Index_2 = this.m_ConvertBones.ConvertBoneIndex((short)m_BlendIndices_in.Index_2, BoneSide, true, ref ErrorLog);
					m_BlendIndices_out.Index_3 = this.m_ConvertBones.ConvertBoneIndex((short)m_BlendIndices_in.Index_3, BoneSide, true, ref ErrorLog);
					m_BlendIndices_out.Index_4 = this.m_ConvertBones.ConvertBoneIndex((short)m_BlendIndices_in.Index_4, BoneSide, true, ref ErrorLog);
				}
				return m_BlendIndices_out;
			}
		}

		// Token: 0x060002BA RID: 698 RVA: 0x0003A8CC File Offset: 0x00038ACC
		private Rx3IndexBuffer[] ConvertRx3IndexBuffers(Rx3IndexBuffer[] Rx3IndexBuffers_in)
		{
			checked
			{
				Rx3IndexBuffer[] Rx3IndexBuffers_out = new Rx3IndexBuffer[Rx3IndexBuffers_in.Length - 1 + 1];
				int num = Rx3IndexBuffers_out.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					long b_in = (long)(unchecked((ulong)this.Id_in[b]));
					Rx3IndexBuffers_out[b] = new Rx3IndexBuffer();
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader = new Rx3IndexBufferHeader();
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader.TotalSize = Rx3IndexBuffers_in[(int)b_in].Rx3IndexBufferHeader.TotalSize;
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader.NumIndices = Rx3IndexBuffers_in[(int)b_in].Rx3IndexBufferHeader.NumIndices;
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader.IndexSize = Rx3IndexBuffers_in[(int)b_in].Rx3IndexBufferHeader.IndexSize;
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader.Padding = new byte[7];
					Rx3IndexBuffers_out[b].IndexStream = Rx3IndexBuffers_in[(int)b_in].IndexStream;
				}
				return Rx3IndexBuffers_out;
			}
		}

		// Token: 0x060002BB RID: 699 RVA: 0x0003A9A4 File Offset: 0x00038BA4
		private Rx3IndexBuffer[] ConvertRx3IndexBuffers(Rx2IndexBuffer[] Rx2IndexBuffers_in, RWGObjectType_IndexBuffer[] RWIndexBuffers_in)
		{
			checked
			{
				Rx3IndexBuffer[] Rx3IndexBuffers_out = new Rx3IndexBuffer[Rx2IndexBuffers_in.Length - 1 + 1];
				int num = Rx3IndexBuffers_out.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					long b_in = (long)(unchecked((ulong)this.Id_in[b]));
					Rx3IndexBuffers_out[b] = new Rx3IndexBuffer();
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader = new Rx3IndexBufferHeader();
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader.TotalSize = 0U;
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader.NumIndices = (uint)Rx2IndexBuffers_in[(int)b_in].IndexStream.Length;
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader.IndexSize = RWIndexBuffers_in[(int)b_in].GetIndexSize();
					Rx3IndexBuffers_out[b].Rx3IndexBufferHeader.Padding = new byte[7];
					Rx3IndexBuffers_out[b].IndexStream = Rx2IndexBuffers_in[(int)b_in].IndexStream;
				}
				return Rx3IndexBuffers_out;
			}
		}

		// Token: 0x060002BC RID: 700 RVA: 0x0003AA68 File Offset: 0x00038C68
		private Rx3BoneRemap[] ConvertRx3BoneRemaps(int NumBoneRemaps)
		{
			checked
			{
				Rx3BoneRemap[] Rx3BoneRemaps_out = new Rx3BoneRemap[NumBoneRemaps - 1 + 1];
				int num = Rx3BoneRemaps_out.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					Rx3BoneRemaps_out[b] = new Rx3BoneRemap
					{
						TotalSize = 528U,
						NumUsedBones = 0,
						Padding = new byte[11],
						UsedBones = new byte[256],
						UsedBonesPositions = new byte[256]
					};
				}
				return Rx3BoneRemaps_out;
			}
		}

		// Token: 0x060002BD RID: 701 RVA: 0x0003AAF0 File Offset: 0x00038CF0
		private ObjectType_AnimationSkin[] UpdateRW4AnimationSkins(int BoneIndex_in, int BoneIndex_out, Rx3AnimationSkin[] Rx3AnimationSkins_in, ObjectType_AnimationSkin[] RW4AnimationSkins_out)
		{
			checked
			{
				int num = RW4AnimationSkins_out.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					RW4AnimationSkins_out[b].BoneMatrices[BoneIndex_out] = Rx3AnimationSkins_in[b].BoneMatrices[BoneIndex_in];
				}
				return RW4AnimationSkins_out;
			}
		}

		// Token: 0x060002BE RID: 702 RVA: 0x0003AB38 File Offset: 0x00038D38
		private Rx3AnimationSkin[] UpdateRx3AnimationSkins(int BoneIndex_in, int BoneIndex_out, Rx3AnimationSkin[] Rx3AnimationSkins_in, Rx3AnimationSkin[] Rx3AnimationSkins_out)
		{
			checked
			{
				int num = Rx3AnimationSkins_out.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					Rx3AnimationSkins_out[b].BoneMatrices[BoneIndex_out] = Rx3AnimationSkins_in[b].BoneMatrices[BoneIndex_in];
				}
				return Rx3AnimationSkins_out;
			}
		}

		// Token: 0x060002BF RID: 703 RVA: 0x000087AB File Offset: 0x000069AB
		private void ConvertRx3AnimationSkins()
		{
		}

		// Token: 0x060002C0 RID: 704 RVA: 0x0003AB80 File Offset: 0x00038D80
		private RW4Section UpdateRW4Section(RW4Section RW4Section_in, RW4Section RW4Section_out)
		{
			bool flag = (RW4Section_in.RW4Skeletons != null & RW4Section_out.RW4Skeletons != null) && RW4Section_in.RW4Skeletons.Length != RW4Section_out.RW4Skeletons.Length;
			checked
			{
				if (flag)
				{
					int StartIndex = RW4Section_out.RW4Skeletons.Length - 1;
					RW4Section_out.RW4Skeletons = (ObjectType_Skeleton[])Utils.CopyArray(RW4Section_out.RW4Skeletons, new ObjectType_Skeleton[RW4Section_in.RW4Skeletons.Length - 1 + 1]);
					bool flag2 = StartIndex + 1 <= RW4Section_out.RW4Skeletons.Length - 1;
					if (flag2)
					{
						int num = StartIndex + 1;
						int num2 = RW4Section_out.RW4Skeletons.Length - 1;
						for (int b = num; b <= num2; b++)
						{
							RW4Section_out.RW4Skeletons[b] = RW4Section_out.RW4Skeletons[0];
						}
					}
				}
				bool flag3 = (RW4Section_in.RW4AnimationSkins != null & RW4Section_out.RW4AnimationSkins != null) && RW4Section_in.RW4AnimationSkins.Length != RW4Section_out.RW4AnimationSkins.Length;
				if (flag3)
				{
					int StartIndex2 = RW4Section_out.RW4AnimationSkins.Length - 1;
					RW4Section_out.RW4AnimationSkins = (ObjectType_AnimationSkin[])Utils.CopyArray(RW4Section_out.RW4AnimationSkins, new ObjectType_AnimationSkin[RW4Section_in.RW4AnimationSkins.Length - 1 + 1]);
					bool flag4 = StartIndex2 + 1 <= RW4Section_out.RW4AnimationSkins.Length - 1;
					if (flag4)
					{
						int num3 = StartIndex2 + 1;
						int num4 = RW4Section_out.RW4AnimationSkins.Length - 1;
						for (int b2 = num3; b2 <= num4; b2++)
						{
							RW4Section_out.RW4AnimationSkins[b2] = RW4Section_out.RW4AnimationSkins[StartIndex2];
						}
					}
				}
				bool flag5 = (RW4Section_in.RW4SkinMatrixBuffers != null & RW4Section_out.RW4SkinMatrixBuffers != null) && RW4Section_in.RW4SkinMatrixBuffers.Length != RW4Section_out.RW4SkinMatrixBuffers.Length;
				if (flag5)
				{
					int StartIndex3 = RW4Section_out.RW4SkinMatrixBuffers.Length - 1;
					RW4Section_out.RW4SkinMatrixBuffers = (ObjectType_SkinMatrixBuffer[])Utils.CopyArray(RW4Section_out.RW4SkinMatrixBuffers, new ObjectType_SkinMatrixBuffer[RW4Section_in.RW4SkinMatrixBuffers.Length - 1 + 1]);
					bool flag6 = StartIndex3 + 1 <= RW4Section_out.RW4SkinMatrixBuffers.Length - 1;
					if (flag6)
					{
						int num5 = StartIndex3 + 1;
						int num6 = RW4Section_out.RW4SkinMatrixBuffers.Length - 1;
						for (int b3 = num5; b3 <= num6; b3++)
						{
							RW4Section_out.RW4SkinMatrixBuffers[b3] = RW4Section_out.RW4SkinMatrixBuffers[StartIndex3];
						}
					}
				}
				RW4Section_in.RW4Skeletons = RW4Section_out.RW4Skeletons;
				RW4Section_in.RW4AnimationSkins = RW4Section_out.RW4AnimationSkins;
				RW4Section_in.RW4SkinMatrixBuffers = RW4Section_out.RW4SkinMatrixBuffers;
				return RW4Section_in;
			}
		}

		// Token: 0x060002C1 RID: 705 RVA: 0x0003ADF4 File Offset: 0x00038FF4
		private EA_FxShader_FxRenderableSimple[] UpdateRW4Shader_0XEF0004(Rx3SimpleMesh[] Rx3SimpleMeshes_in, EA_FxShader_FxRenderableSimple[] RW4Shader_out)
		{
			checked
			{
				int num = RW4Shader_out.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					long b_in = (long)(unchecked((ulong)this.Id_in[b]));
					RW4Shader_out[b].PrimitiveType = Rx3SimpleMeshes_in[(int)b_in].PrimitiveType;
				}
				return RW4Shader_out;
			}
		}

		// Token: 0x060002C2 RID: 706 RVA: 0x0003AE38 File Offset: 0x00039038
		private EA_FxShader_FxRenderableSimple[] UpdateRW4Shader_0XEF0004(EA_FxShader_FxRenderableSimple[] RW4Shader_in)
		{
			checked
			{
				EA_FxShader_FxRenderableSimple[] RW4Shader_out = new EA_FxShader_FxRenderableSimple[RW4Shader_in.Length - 1 + 1];
				int num = RW4Shader_out.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					long b_in = (long)(unchecked((ulong)this.Id_in[b]));
					RW4Shader_out[b] = RW4Shader_in[(int)b_in];
				}
				return RW4Shader_out;
			}
		}

		// Token: 0x060002C3 RID: 707 RVA: 0x0003AE80 File Offset: 0x00039080
		private EA_ArenaDictionary UpdateRW4NameSection(EA_ArenaDictionary RW4NameSection_in, EA_ArenaDictionary RW4NameSection_out)
		{
			NameTable[] NameTable_in = RW4NameSection_in.GetNameTable();
			NameTable[] NameTable_out = RW4NameSection_out.GetNameTable();
			NameTable[] ReturnNameTable = this.UpdateNameTable(NameTable_in, NameTable_out, this.m_GameType_in, this.m_GameType_out);
			bool flag = RW4NameSection_out.Names.Length == ReturnNameTable.Length;
			checked
			{
				if (flag)
				{
					int num = RW4NameSection_out.Names.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						RW4NameSection_out.Names[i].Name = ReturnNameTable[i].Name;
						RW4NameSection_out.Names[i].ObjectId = (RWSectionCode)ReturnNameTable[i].ObjectId;
						RW4NameSection_out.Names[i].Offset = 0U;
					}
				}
				return RW4NameSection_out;
			}
		}

		// Token: 0x060002C4 RID: 708 RVA: 0x0003AF28 File Offset: 0x00039128
		private EA_ArenaDictionary UpdateRW4NameSection(Rx3NameTable Rx3NameTable_in, EA_ArenaDictionary RW4NameSection_out)
		{
			NameTable[] NameTable_in = Rx3NameTable_in.GetNameTable();
			NameTable[] NameTable_out = RW4NameSection_out.GetNameTable();
			NameTable[] ReturnNameTable = this.UpdateNameTable(NameTable_in, NameTable_out, this.m_GameType_in, this.m_GameType_out);
			bool flag = RW4NameSection_out.Names.Length == ReturnNameTable.Length;
			checked
			{
				if (flag)
				{
					int num = RW4NameSection_out.Names.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						RW4NameSection_out.Names[i].Name = ReturnNameTable[i].Name;
						RW4NameSection_out.Names[i].ObjectId = (RWSectionCode)ReturnNameTable[i].ObjectId;
						RW4NameSection_out.Names[i].Offset = 0U;
					}
				}
				return RW4NameSection_out;
			}
		}

		// Token: 0x060002C5 RID: 709 RVA: 0x0003AFD0 File Offset: 0x000391D0
		private Rx3NameTable UpdateRx3NameSection(Rx3NameTable Rx3NameTable_in, Rx3NameTable Rx3NameTable_out)
		{
			NameTable[] NameTable_in = Rx3NameTable_in.GetNameTable();
			NameTable[] NameTable_out = Rx3NameTable_out.GetNameTable();
			NameTable[] ReturnNameTable = this.UpdateNameTable(NameTable_in, NameTable_out, this.m_GameType_in, this.m_GameType_out);
			checked
			{
				Rx3NameTable_out.NumNames = (uint)ReturnNameTable.Length;
				Rx3NameTable_out.Names = new Rx3Name[(int)(unchecked((ulong)Rx3NameTable_out.NumNames) - 1UL) + 1];
				int num = Rx3NameTable_out.Names.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					Rx3NameTable_out.Names[i] = new Rx3Name
					{
						Name = ReturnNameTable[i].Name,
						ObjectId = (Rx3SectionHash)ReturnNameTable[i].ObjectId,
						NameSize = (uint)(ReturnNameTable[i].Name.Length + 1)
					};
				}
				return Rx3NameTable_out;
			}
		}

		// Token: 0x060002C6 RID: 710 RVA: 0x0003B094 File Offset: 0x00039294
		private Rx3NameTable UpdateRx3NameSection(EA_ArenaDictionary RW4NameSection_in, EA_FxShader_FxRenderableSimple[] RW4Shader_FxRenderableSimples_in, Rx3NameTable Rx3NameTable_out)
		{
			bool flag = RW4NameSection_in != null && RW4NameSection_in.NumNames > 0;
			checked
			{
				NameTable[] NameTable_in;
				if (flag)
				{
					NameTable_in = RW4NameSection_in.GetNameTable();
				}
				else
				{
					NameTable_in = new NameTable[RW4Shader_FxRenderableSimples_in.Length - 1 + 1];
					int num = NameTable_in.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						NameTable_in[i] = new NameTable
						{
							ObjectId = 15663108U,
							Name = RW4Shader_FxRenderableSimples_in[i].String_1 + ".FxRenderableSimple"
						};
					}
				}
				NameTable[] NameTable_out = Rx3NameTable_out.GetNameTable();
				NameTable[] ReturnNameTable = this.UpdateNameTable(NameTable_in, NameTable_out, this.m_GameType_in, this.m_GameType_out);
				Rx3NameTable_out.NumNames = (uint)ReturnNameTable.Length;
				Rx3NameTable_out.Names = new Rx3Name[(int)(unchecked((ulong)Rx3NameTable_out.NumNames) - 1UL) + 1];
				int num2 = Rx3NameTable_out.Names.Length - 1;
				for (int j = 0; j <= num2; j++)
				{
					Rx3NameTable_out.Names[j] = new Rx3Name
					{
						Name = ReturnNameTable[j].Name,
						ObjectId = (Rx3SectionHash)ReturnNameTable[j].ObjectId,
						NameSize = (uint)(ReturnNameTable[j].Name.Length + 1)
					};
				}
				return Rx3NameTable_out;
			}
		}

		// Token: 0x060002C7 RID: 711 RVA: 0x0003B1C8 File Offset: 0x000393C8
		private NameTable[] UpdateNameTable(NameTable[] NameTable_in, NameTable[] NameTable_out, General.EGameType GameType_in, General.EGameType GameType_out)
		{
			checked
			{
				switch (this.m_FileType)
				{
				case General.EFileType.HEAD_MODEL:
				{
					NameTable_out = (NameTable[])Utils.CopyArray(NameTable_out, new NameTable[NameTable_in.Length - 1 + 1]);
					int num = NameTable_out.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag = NameTable_in[i].ObjectId == 3566041216U | NameTable_in[i].ObjectId == 15663108U;
						if (flag)
						{
							long b_in = (long)(unchecked((ulong)this.Id_in[i]));
							NameTable_out[i] = new NameTable();
							NameTable_out[i].Name = NameTable_in[(int)b_in].Name;
							bool flag2 = (NameTable_out[i].Name.Contains("eyes") | NameTable_out[i].Name.Contains("eyel") | NameTable_out[i].Name.Contains("eyer")) & !NameTable_out[i].Name.Contains("eyelashes");
							if (flag2)
							{
								bool flag3 = GameType_out == General.EGameType.FIFA_15 | GameType_out == General.EGameType.FIFA_16;
								if (flag3)
								{
									NameTable_out[i].Name = "eyes.FxRenderableSimple";
								}
								else
								{
									NameTable_out[i].Name = "eyes_.FxRenderableSimple";
								}
							}
							else
							{
								bool flag4 = (NameTable_out[i].Name.Contains("head") | NameTable_out[i].Name.Contains("mouthbag") | NameTable_out[i].Name.Contains("eyelashes")) & !NameTable_out[i].Name.Contains("eyes");
								if (flag4)
								{
									bool flag5 = GameType_out == General.EGameType.FIFA_15 | GameType_out == General.EGameType.FIFA_16;
									if (flag5)
									{
										NameTable_out[i].Name = "head.FxRenderableSimple";
									}
									else
									{
										NameTable_out[i].Name = "head_.FxRenderableSimple";
									}
								}
							}
							bool flag6 = this.m_FileFormat_out == General.EFileFormat.RX3;
							if (flag6)
							{
								NameTable_out[i].ObjectId = 3566041216U;
							}
							else
							{
								NameTable_out[i].ObjectId = 15663108U;
							}
						}
					}
					return NameTable_out;
				}
				case General.EFileType.HAIR_MODEL:
				{
					string[] StrList = null;
					int NumFound = 0;
					int num2 = NameTable_in.Length - 1;
					for (int j = 0; j <= num2; j++)
					{
						bool flag7 = NameTable_in[j].ObjectId == 3566041216U | NameTable_in[j].ObjectId == 15663108U;
						if (flag7)
						{
							NumFound++;
							StrList = (string[])Utils.CopyArray(StrList, new string[NumFound - 1 + 1]);
							StrList[NumFound - 1] = NameTable_in[j].Name;
						}
					}
					int NumFound2 = 0;
					int NumCurrent = 0;
					NameTable_out = null;
					int num3 = NameTable_in.Length - 1;
					for (int k = 0; k <= num3; k++)
					{
						bool flag8 = NameTable_in[k].ObjectId == 3566041216U | NameTable_in[k].ObjectId == 15663108U;
						if (flag8)
						{
							long b_in2 = (long)(unchecked((ulong)this.Id_in[NumFound2]));
							NumFound2++;
							NumCurrent++;
							NameTable_out = (NameTable[])Utils.CopyArray(NameTable_out, new NameTable[NumCurrent - 1 + 1]);
							NameTable_out[NumCurrent - 1] = new NameTable();
							NameTable_out[NumCurrent - 1].Name = StrList[(int)b_in2];
							bool flag9 = NameTable_out[NumCurrent - 1].Name.Contains("player_hair_kk_alphaA");
							if (flag9)
							{
								bool flag10 = GameType_out == General.EGameType.FIFA_15 | GameType_out == General.EGameType.FIFA_16;
								if (flag10)
								{
									NameTable_out[NumCurrent - 1].Name = "player_hair_kk_alphaA.FxRenderableSimple";
								}
								else
								{
									NameTable_out[NumCurrent - 1].Name = "player_hair_kk_alphaA_.FxRenderableSimple";
								}
							}
							else
							{
								bool flag11 = NameTable_out[NumCurrent - 1].Name.Contains("player_hair_kk_alphaB");
								if (flag11)
								{
									bool flag12 = GameType_out == General.EGameType.FIFA_15 | GameType_out == General.EGameType.FIFA_16;
									if (flag12)
									{
										NameTable_out[NumCurrent - 1].Name = "player_hair_kk_alphaB.FxRenderableSimple";
									}
									else
									{
										NameTable_out[NumCurrent - 1].Name = "player_hair_kk_alphaB_.FxRenderableSimple";
									}
								}
							}
							bool flag13 = this.m_FileFormat_out == General.EFileFormat.RX3;
							if (flag13)
							{
								NameTable_out[NumCurrent - 1].ObjectId = 3566041216U;
							}
							else
							{
								NameTable_out[NumCurrent - 1].ObjectId = 15663108U;
							}
						}
						else
						{
							bool flag14 = !General.HasOldNameTableFormat(GameType_out);
							if (flag14)
							{
								NumCurrent++;
								NameTable_out = (NameTable[])Utils.CopyArray(NameTable_out, new NameTable[NumCurrent - 1 + 1]);
								NameTable_out[NumCurrent - 1] = new NameTable();
								NameTable_out[NumCurrent - 1].Name = NameTable_in[k].Name;
								NameTable_out[NumCurrent - 1].ObjectId = 0U;
							}
						}
					}
					return NameTable_out;
				}
				case General.EFileType.HAIR_LOD_MODEL:
					NameTable_out = (NameTable[])Utils.CopyArray(NameTable_out, new NameTable[1]);
					NameTable_out[0].Name = "player_hair_kk_alphaA_lod.FxRenderableSimple";
					return NameTable_out;
				case General.EFileType.SHOE_MODEL:
					NameTable_out = (NameTable[])Utils.CopyArray(NameTable_out, new NameTable[1]);
					NameTable_out[0].Name = "shoe_.FxRenderableSimple";
					return NameTable_out;
				case General.EFileType.BALL_MODEL:
					NameTable_out = (NameTable[])Utils.CopyArray(NameTable_out, new NameTable[1]);
					NameTable_out[0].Name = "ball_.FxRenderableSimple";
					return NameTable_out;
				}
				NameTable_out = new NameTable[NameTable_in.Length - 1 + 1];
				int num4 = NameTable_out.Length - 1;
				for (int l = 0; l <= num4; l++)
				{
					NameTable_out[l] = new NameTable();
					long b_in3;
					unchecked
					{
						b_in3 = (long)l;
						bool flag15 = this.Id_in.Length == NameTable_out.Length;
						if (flag15)
						{
							b_in3 = (long)((ulong)this.Id_in[l]);
						}
					}
					NameTable_out[l].Name = NameTable_in[(int)b_in3].Name;
					bool flag16 = NameTable_in[(int)b_in3].ObjectId == 3566041216U | NameTable_in[(int)b_in3].ObjectId == 15663108U;
					if (flag16)
					{
						bool flag17 = this.m_FileFormat_out == General.EFileFormat.RX3;
						if (flag17)
						{
							NameTable_out[l].ObjectId = 3566041216U;
						}
						else
						{
							NameTable_out[l].ObjectId = 15663108U;
						}
					}
					else
					{
						NameTable_out[l].ObjectId = 0U;
					}
				}
				return NameTable_out;
			}
		}

		// Token: 0x060002C8 RID: 712 RVA: 0x0003B790 File Offset: 0x00039990
		private Rx3VertexFormat[] UpdateRx3VertexFormats(RWGObjectType_VertexDescriptor[] RW4VertexDescriptor_in, Rx3VertexFormat[] Rx3VertexFormats_out, ref Rx3VertexBuffer[] Rx3VertexBuffers_out, bool BoneIndicesHasShort_in, bool BoneIndicesHasShort_out, bool UpdateVFormat)
		{
			checked
			{
				if (UpdateVFormat)
				{
					Rx3VertexFormats_out = (Rx3VertexFormat[])Utils.CopyArray(Rx3VertexFormats_out, new Rx3VertexFormat[RW4VertexDescriptor_in.Length - 1 + 1]);
					int num = Rx3VertexFormats_out.Length - 1;
					for (int b = 0; b <= num; b++)
					{
						long b_in = (long)(unchecked((ulong)this.Id_in[b]));
						Rx3VertexFormats_out[b] = this.VertexFormat_RW4ToRx3(RW4VertexDescriptor_in[(int)b_in]);
						D3DDECLTYPE BoneIndicesType_in = this.GetBoneIndicesDataType(RW4VertexDescriptor_in[(int)b_in]);
						D3DDECLTYPE BoneIndicesType_out = BoneIndicesHasShort_out ? D3DDECLTYPE.USHORT4 : D3DDECLTYPE.UBYTE4;
						bool flag = BoneIndicesType_in == D3DDECLTYPE.UBYTE4 & BoneIndicesType_out == D3DDECLTYPE.USHORT4;
						if (flag)
						{
							Rx3VertexFormats_out[b] = this.BoneIndicesToShort(Rx3VertexFormats_out[b], ref Rx3VertexBuffers_out[b]);
						}
						else
						{
							bool flag2 = BoneIndicesType_in == D3DDECLTYPE.USHORT4 & BoneIndicesType_out == D3DDECLTYPE.UBYTE4;
							if (flag2)
							{
								Rx3VertexFormats_out[b] = this.BoneIndicesToByte(Rx3VertexFormats_out[b], ref Rx3VertexBuffers_out[b]);
							}
						}
						unchecked
						{
							bool flag3 = this.m_FileType == General.EFileType.HEAD_MODEL & (this.m_GameType_out == General.EGameType.FIFA_15 | this.m_GameType_out == General.EGameType.FIFA_16 | General.IsGameFrostbiteEngine(this.m_GameType_out)) & this.GetNumBlendIndicesInVertex((long)b, Rx3VertexFormats_out) == 1;
							if (flag3)
							{
								Rx3VertexFormats_out[b] = this.NumBonesSetsTo2(Rx3VertexFormats_out[b], ref Rx3VertexBuffers_out[b]);
							}
							else
							{
								bool flag4 = this.m_FileType == General.EFileType.HEAD_MODEL & (this.m_GameType_out != General.EGameType.FIFA_15 & this.m_GameType_out != General.EGameType.FIFA_16 & !General.IsGameFrostbiteEngine(this.m_GameType_out)) & this.GetNumBlendIndicesInVertex((long)b, Rx3VertexFormats_out) == 2;
								if (flag4)
								{
									Rx3VertexFormats_out[b] = this.NumBonesSetsTo1(Rx3VertexFormats_out[b], ref Rx3VertexBuffers_out[b]);
								}
							}
						}
					}
				}
				return Rx3VertexFormats_out;
			}
		}

		// Token: 0x060002C9 RID: 713 RVA: 0x0003B938 File Offset: 0x00039B38
		private Rx3VertexFormat[] UpdateRx3VertexFormats(Rx3VertexFormat[] Rx3VertexFormats_in, Rx3VertexFormat[] Rx3VertexFormats_out, ref Rx3VertexBuffer[] Rx3VertexBuffers_out, bool BoneIndicesHasShort_in, bool BoneIndicesHasShort_out, bool UpdateVFormat)
		{
			checked
			{
				if (UpdateVFormat)
				{
					Rx3VertexFormats_out = (Rx3VertexFormat[])Utils.CopyArray(Rx3VertexFormats_out, new Rx3VertexFormat[Rx3VertexFormats_in.Length - 1 + 1]);
					int num = Rx3VertexFormats_out.Length - 1;
					for (int b = 0; b <= num; b++)
					{
						long b_in = (long)(unchecked((ulong)this.Id_in[b]));
						Rx3VertexFormats_out[b] = Rx3VertexFormats_in[(int)b_in];
						D3DDECLTYPE BoneIndicesType_in = this.GetBoneIndicesDataType(Rx3VertexFormats_in[(int)b_in]);
						D3DDECLTYPE BoneIndicesType_out = BoneIndicesHasShort_out ? D3DDECLTYPE.USHORT4 : D3DDECLTYPE.UBYTE4;
						bool flag = BoneIndicesType_in == D3DDECLTYPE.UBYTE4 & BoneIndicesType_out == D3DDECLTYPE.USHORT4;
						if (flag)
						{
							Rx3VertexFormats_out[b] = this.BoneIndicesToShort(Rx3VertexFormats_out[b], ref Rx3VertexBuffers_out[b]);
						}
						else
						{
							bool flag2 = BoneIndicesType_in == D3DDECLTYPE.USHORT4 & BoneIndicesType_out == D3DDECLTYPE.UBYTE4;
							if (flag2)
							{
								Rx3VertexFormats_out[b] = this.BoneIndicesToByte(Rx3VertexFormats_out[b], ref Rx3VertexBuffers_out[b]);
							}
						}
						unchecked
						{
							bool flag3 = this.m_FileType == General.EFileType.HEAD_MODEL & (this.m_GameType_out == General.EGameType.FIFA_15 | this.m_GameType_out == General.EGameType.FIFA_16 | General.IsGameFrostbiteEngine(this.m_GameType_out)) & this.GetNumBlendIndicesInVertex((long)b, Rx3VertexFormats_out) == 1;
							if (flag3)
							{
								Rx3VertexFormats_out[b] = this.NumBonesSetsTo2(Rx3VertexFormats_out[b], ref Rx3VertexBuffers_out[b]);
							}
							else
							{
								bool flag4 = this.m_FileType == General.EFileType.HEAD_MODEL & (this.m_GameType_out != General.EGameType.FIFA_15 & this.m_GameType_out != General.EGameType.FIFA_16 & !General.IsGameFrostbiteEngine(this.m_GameType_out)) & this.GetNumBlendIndicesInVertex((long)b, Rx3VertexFormats_out) == 2;
								if (flag4)
								{
									Rx3VertexFormats_out[b] = this.NumBonesSetsTo1(Rx3VertexFormats_out[b], ref Rx3VertexBuffers_out[b]);
								}
							}
						}
					}
				}
				return Rx3VertexFormats_out;
			}
		}

		// Token: 0x060002CA RID: 714 RVA: 0x0003BADC File Offset: 0x00039CDC
		private Rx3VertexFormat UpdateRx3VertexFormat_UNUSED(Rx3VertexFormat Rx3VertexFormat, ref Rx3VertexBuffer Rx3VertexBuffer, bool BoneIndicesHasShort_in, bool BoneIndicesHasShort_out)
		{
			bool flag = !BoneIndicesHasShort_in && BoneIndicesHasShort_out;
			if (flag)
			{
				Rx3VertexFormat = this.BoneIndicesToShort(Rx3VertexFormat, ref Rx3VertexBuffer);
			}
			else
			{
				bool flag2 = BoneIndicesHasShort_in & !BoneIndicesHasShort_out;
				if (flag2)
				{
					Rx3VertexFormat = this.BoneIndicesToByte(Rx3VertexFormat, ref Rx3VertexBuffer);
				}
			}
			bool flag3 = this.m_FileType == General.EFileType.HEAD_MODEL & (this.m_GameType_out == General.EGameType.FIFA_15 | this.m_GameType_out == General.EGameType.FIFA_16 | General.IsGameFrostbiteEngine(this.m_GameType_out)) & this.NumBlendIndicesInVertex(Rx3VertexFormat) == 1;
			if (flag3)
			{
				Rx3VertexFormat = this.NumBonesSetsTo2(Rx3VertexFormat, ref Rx3VertexBuffer);
			}
			else
			{
				bool flag4 = this.m_FileType == General.EFileType.HEAD_MODEL & (this.m_GameType_out != General.EGameType.FIFA_15 & this.m_GameType_out != General.EGameType.FIFA_16 & !General.IsGameFrostbiteEngine(this.m_GameType_out)) & this.NumBlendIndicesInVertex(Rx3VertexFormat) == 2;
				if (flag4)
				{
					Rx3VertexFormat = this.NumBonesSetsTo1(Rx3VertexFormat, ref Rx3VertexBuffer);
				}
			}
			return Rx3VertexFormat;
		}

		// Token: 0x060002CB RID: 715 RVA: 0x0003BBB4 File Offset: 0x00039DB4
		private Rx3VertexFormat VertexFormat_RW4ToRx3(RWGObjectType_VertexDescriptor RW4VertexDescriptor_in)
		{
			Rx3VertexFormat Rx3VertexFormat_out = new Rx3VertexFormat();
			Rx3VertexFormat_out.TotalSize = 0U;
			Rx3VertexFormat_out.VertexFormatSize = 0U;
			Rx3VertexFormat_out.Padding = new uint[2];
			checked
			{
				Rx3VertexFormat_out.Elements = new Rx3VertexElement[RW4VertexDescriptor_in.Elements.Length - 1 + 1];
				Rx3VertexFormat_out.VertexFormat = new string[RW4VertexDescriptor_in.Elements.Length - 1 + 1];
				int num = Rx3VertexFormat_out.Elements.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					Rx3VertexFormat_out.Elements[i] = new Rx3VertexElement
					{
						DataType = RW4VertexDescriptor_in.Elements[i].DataType,
						Offset = (uint)RW4VertexDescriptor_in.Elements[i].Offset,
						Usage = RW4VertexDescriptor_in.Elements[i].Usage,
						UsageIndex = (uint)RW4VertexDescriptor_in.Elements[i].UsageIndex
					};
					Rx3VertexFormat_out.VertexFormat[i] = Rx3VertexFormat_out.Elements[i].ToVertexFormatString("00:00:00:0001:0000");
				}
				return Rx3VertexFormat_out;
			}
		}

		// Token: 0x060002CC RID: 716 RVA: 0x0003BCB8 File Offset: 0x00039EB8
		private Rx3VertexFormat NumBonesSetsTo1(Rx3VertexFormat m_Rx3VertexFormat, ref Rx3VertexBuffer m_Rx3VertexBuffer)
		{
			int NumFound = 0;
			int ChangedSize = 0;
			Rx3VertexElement[] Tmp_Elements = m_Rx3VertexFormat.Elements;
			string[] Tmp_VertexFormat = m_Rx3VertexFormat.VertexFormat;
			checked
			{
				m_Rx3VertexFormat.Elements = new Rx3VertexElement[m_Rx3VertexFormat.Elements.Length - 1 - 2 + 1];
				m_Rx3VertexFormat.VertexFormat = new string[m_Rx3VertexFormat.VertexFormat.Length - 1 - 2 + 1];
				int num = Tmp_Elements.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = (Tmp_Elements[i].Usage == DeclarationUsage.BlendIndices | Tmp_Elements[i].Usage == DeclarationUsage.BlendWeight) && unchecked((ulong)Tmp_Elements[i].UsageIndex) == 1UL;
					if (flag)
					{
						bool flag2 = Tmp_Elements[i].Usage == DeclarationUsage.BlendIndices;
						if (flag2)
						{
							bool flag3 = Tmp_Elements[i].DataType == D3DDECLTYPE.UBYTE4;
							if (flag3)
							{
								ChangedSize -= 4;
							}
							else
							{
								bool flag4 = Tmp_Elements[i].DataType == D3DDECLTYPE.USHORT4;
								if (flag4)
								{
									ChangedSize -= 8;
								}
							}
						}
						else
						{
							bool flag5 = Tmp_Elements[i].Usage == DeclarationUsage.BlendWeight;
							if (flag5)
							{
								ChangedSize -= 4;
							}
						}
						NumFound++;
					}
					else
					{
						m_Rx3VertexFormat.Elements[i - NumFound] = new Rx3VertexElement();
						m_Rx3VertexFormat.Elements[i - NumFound].UsageIndex = Tmp_Elements[i].UsageIndex;
						m_Rx3VertexFormat.Elements[i - NumFound].DataType = Tmp_Elements[i].DataType;
						m_Rx3VertexFormat.Elements[i - NumFound].Offset = (uint)(unchecked((ulong)Tmp_Elements[i].Offset) + (ulong)(unchecked((long)ChangedSize)));
						m_Rx3VertexFormat.Elements[i - NumFound].Usage = Tmp_Elements[i].Usage;
						m_Rx3VertexFormat.VertexFormat[i - NumFound] = m_Rx3VertexFormat.Elements[i - NumFound].ToVertexFormatString(Tmp_VertexFormat[i]);
					}
				}
				m_Rx3VertexBuffer.VertexSize = (uint)(unchecked((ulong)m_Rx3VertexBuffer.VertexSize) + (ulong)(unchecked((long)ChangedSize)));
				return m_Rx3VertexFormat;
			}
		}

		// Token: 0x060002CD RID: 717 RVA: 0x0003BE84 File Offset: 0x0003A084
		private Rx3VertexFormat NumBonesSetsTo2(Rx3VertexFormat m_Rx3VertexFormat, ref Rx3VertexBuffer m_Rx3VertexBuffer)
		{
			int NumFound = 0;
			int ChangedSize = 0;
			Rx3VertexElement[] Tmp_Elements = m_Rx3VertexFormat.Elements;
			string[] Tmp_VertexFormat = m_Rx3VertexFormat.VertexFormat;
			checked
			{
				m_Rx3VertexFormat.Elements = new Rx3VertexElement[m_Rx3VertexFormat.Elements.Length - 1 + 2 + 1];
				m_Rx3VertexFormat.VertexFormat = new string[m_Rx3VertexFormat.VertexFormat.Length - 1 + 2 + 1];
				int num = m_Rx3VertexFormat.Elements.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					m_Rx3VertexFormat.Elements[i] = new Rx3VertexElement();
					bool flag = i > 0 && (m_Rx3VertexFormat.Elements[i - 1].Usage == DeclarationUsage.BlendIndices | m_Rx3VertexFormat.Elements[i - 1].Usage == DeclarationUsage.BlendWeight) && unchecked((ulong)m_Rx3VertexFormat.Elements[checked(i - 1)].UsageIndex) == 0UL;
					if (flag)
					{
						NumFound++;
						bool flag2 = Tmp_Elements[i - NumFound].Usage == DeclarationUsage.BlendIndices;
						if (flag2)
						{
							bool flag3 = Tmp_Elements[i - NumFound].DataType == D3DDECLTYPE.UBYTE4;
							if (flag3)
							{
								ChangedSize += 4;
							}
							else
							{
								bool flag4 = Tmp_Elements[i - NumFound].DataType == D3DDECLTYPE.USHORT4;
								if (flag4)
								{
									ChangedSize += 8;
								}
							}
						}
						else
						{
							bool flag5 = Tmp_Elements[i - NumFound].Usage == DeclarationUsage.BlendWeight;
							if (flag5)
							{
								ChangedSize += 4;
							}
						}
						m_Rx3VertexFormat.Elements[i].UsageIndex = 1U;
					}
					else
					{
						m_Rx3VertexFormat.Elements[i].UsageIndex = Tmp_Elements[i - NumFound].UsageIndex;
					}
					m_Rx3VertexFormat.Elements[i].DataType = Tmp_Elements[i - NumFound].DataType;
					m_Rx3VertexFormat.Elements[i].Offset = (uint)(unchecked((ulong)Tmp_Elements[checked(i - NumFound)].Offset) + (ulong)(unchecked((long)ChangedSize)));
					m_Rx3VertexFormat.Elements[i].Usage = Tmp_Elements[i - NumFound].Usage;
					m_Rx3VertexFormat.VertexFormat[i] = m_Rx3VertexFormat.Elements[i].ToVertexFormatString(Tmp_VertexFormat[i - NumFound]);
				}
				m_Rx3VertexBuffer.VertexSize = (uint)(unchecked((ulong)m_Rx3VertexBuffer.VertexSize) + (ulong)(unchecked((long)ChangedSize)));
				return m_Rx3VertexFormat;
			}
		}

		// Token: 0x060002CE RID: 718 RVA: 0x0003C084 File Offset: 0x0003A284
		private Rx3VertexFormat BoneIndicesToByte(Rx3VertexFormat m_Rx3VertexFormat, ref Rx3VertexBuffer m_Rx3VertexBuffer)
		{
			int NumFound = 0;
			checked
			{
				int num = m_Rx3VertexFormat.Elements.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = NumFound > 0;
					if (flag)
					{
						m_Rx3VertexFormat.Elements[i].Offset = (uint)(unchecked((ulong)m_Rx3VertexFormat.Elements[i].Offset) - (ulong)(unchecked((long)(checked(4 * NumFound)))));
						m_Rx3VertexFormat.VertexFormat[i] = m_Rx3VertexFormat.Elements[i].ToVertexFormatString(m_Rx3VertexFormat.VertexFormat[i]);
					}
					bool flag2 = m_Rx3VertexFormat.Elements[i].Usage == DeclarationUsage.BlendIndices & m_Rx3VertexFormat.Elements[i].DataType == D3DDECLTYPE.USHORT4;
					if (flag2)
					{
						m_Rx3VertexFormat.Elements[i].DataType = D3DDECLTYPE.UBYTE4;
						m_Rx3VertexFormat.VertexFormat[i] = m_Rx3VertexFormat.Elements[i].ToVertexFormatString(m_Rx3VertexFormat.VertexFormat[i]);
						NumFound++;
					}
				}
				m_Rx3VertexBuffer.VertexSize = (uint)(unchecked((ulong)m_Rx3VertexBuffer.VertexSize) - (ulong)(unchecked((long)(checked(4 * NumFound)))));
				return m_Rx3VertexFormat;
			}
		}

		// Token: 0x060002CF RID: 719 RVA: 0x0003C178 File Offset: 0x0003A378
		private Rx3VertexFormat BoneIndicesToShort(Rx3VertexFormat m_Rx3VertexFormat, ref Rx3VertexBuffer m_Rx3VertexBuffer)
		{
			int NumFound = 0;
			checked
			{
				int num = m_Rx3VertexFormat.Elements.Length - 1;
				for (int i = 0; i <= num; i++)
				{
					bool flag = NumFound > 0;
					if (flag)
					{
						m_Rx3VertexFormat.Elements[i].Offset = (uint)(unchecked((ulong)m_Rx3VertexFormat.Elements[i].Offset) + (ulong)(unchecked((long)(checked(4 * NumFound)))));
						m_Rx3VertexFormat.VertexFormat[i] = m_Rx3VertexFormat.Elements[i].ToVertexFormatString(m_Rx3VertexFormat.VertexFormat[i]);
					}
					bool flag2 = m_Rx3VertexFormat.Elements[i].Usage == DeclarationUsage.BlendIndices & m_Rx3VertexFormat.Elements[i].DataType == D3DDECLTYPE.UBYTE4;
					if (flag2)
					{
						m_Rx3VertexFormat.Elements[i].DataType = D3DDECLTYPE.USHORT4;
						m_Rx3VertexFormat.VertexFormat[i] = m_Rx3VertexFormat.Elements[i].ToVertexFormatString(m_Rx3VertexFormat.VertexFormat[i]);
						NumFound++;
					}
				}
				m_Rx3VertexBuffer.VertexSize = (uint)(unchecked((ulong)m_Rx3VertexBuffer.VertexSize) + (ulong)(unchecked((long)(checked(4 * NumFound)))));
				return m_Rx3VertexFormat;
			}
		}

		// Token: 0x060002D0 RID: 720 RVA: 0x0003C26C File Offset: 0x0003A46C
		private bool CheckBoneIndicesHasShort(ObjectType_AnimationSkin m_RW4AnimationSkin)
		{
			return checked(unchecked((ulong)m_RW4AnimationSkin.NumBones) - 1UL) > 255UL;
		}

		// Token: 0x060002D1 RID: 721 RVA: 0x0003C29C File Offset: 0x0003A49C
		private bool CheckBoneIndicesHasShort(Rx3AnimationSkin m_Rx3AnimationSkin)
		{
			return checked(unchecked((ulong)m_Rx3AnimationSkin.NumBones) - 1UL) > 255UL;
		}

		// Token: 0x060002D2 RID: 722 RVA: 0x0003C2CC File Offset: 0x0003A4CC
		private D3DDECLTYPE GetBoneIndicesDataType(RWGObjectType_VertexDescriptor m_RW4VertexDescriptor)
		{
			bool flag = m_RW4VertexDescriptor != null;
			checked
			{
				if (flag)
				{
					int num = m_RW4VertexDescriptor.Elements.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = m_RW4VertexDescriptor.Elements[i].Usage == DeclarationUsage.BlendIndices;
						if (flag2)
						{
							return m_RW4VertexDescriptor.Elements[i].DataType;
						}
					}
				}
				return D3DDECLTYPE.UBYTE4;
			}
		}

		// Token: 0x060002D3 RID: 723 RVA: 0x0003C32C File Offset: 0x0003A52C
		private D3DDECLTYPE GetBoneIndicesDataType(Rx3VertexFormat m_Rx3VertexFormat)
		{
			bool flag = m_Rx3VertexFormat != null;
			checked
			{
				if (flag)
				{
					int num = m_Rx3VertexFormat.Elements.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = m_Rx3VertexFormat.Elements[i].Usage == DeclarationUsage.BlendIndices;
						if (flag2)
						{
							return m_Rx3VertexFormat.Elements[i].DataType;
						}
					}
				}
				return D3DDECLTYPE.UBYTE4;
			}
		}

		// Token: 0x060002D4 RID: 724 RVA: 0x0003C38C File Offset: 0x0003A58C
		public static D3DDECLTYPE GetBoneIndicesDataType(FIFALibrary20.VertexElement[] VertexElements)
		{
			bool flag = VertexElements != null;
			checked
			{
				if (flag)
				{
					int num = VertexElements.Count<FIFALibrary20.VertexElement>() - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = VertexElements[i].Usage == DeclarationUsage.BlendIndices;
						if (flag2)
						{
							return VertexElements[i].DataType;
						}
					}
				}
				return D3DDECLTYPE.UBYTE4;
			}
		}

		// Token: 0x060002D5 RID: 725 RVA: 0x0003C3E0 File Offset: 0x0003A5E0
		private D3DDECLTYPE GetBoneWeightsDataType(RWGObjectType_VertexDescriptor m_RW4VertexDescriptor)
		{
			bool flag = m_RW4VertexDescriptor != null;
			checked
			{
				if (flag)
				{
					int num = m_RW4VertexDescriptor.Elements.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = m_RW4VertexDescriptor.Elements[i].Usage == DeclarationUsage.BlendWeight;
						if (flag2)
						{
							return m_RW4VertexDescriptor.Elements[i].DataType;
						}
					}
				}
				return D3DDECLTYPE.UBYTE4N;
			}
		}

		// Token: 0x060002D6 RID: 726 RVA: 0x0003C440 File Offset: 0x0003A640
		private D3DDECLTYPE GetBoneWeightsDataType(Rx3VertexFormat m_Rx3VertexFormat)
		{
			bool flag = m_Rx3VertexFormat != null;
			checked
			{
				if (flag)
				{
					int num = m_Rx3VertexFormat.Elements.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = m_Rx3VertexFormat.Elements[i].Usage == DeclarationUsage.BlendWeight;
						if (flag2)
						{
							return m_Rx3VertexFormat.Elements[i].DataType;
						}
					}
				}
				return D3DDECLTYPE.UBYTE4N;
			}
		}

		// Token: 0x060002D7 RID: 727 RVA: 0x0003C4A0 File Offset: 0x0003A6A0
		public static D3DDECLTYPE GetBoneWeightsDataType(FIFALibrary20.VertexElement[] VertexElements)
		{
			bool flag = VertexElements != null;
			checked
			{
				if (flag)
				{
					int num = VertexElements.Count<FIFALibrary20.VertexElement>() - 1;
					for (int i = 0; i <= num; i++)
					{
						bool flag2 = VertexElements[i].Usage == DeclarationUsage.BlendWeight;
						if (flag2)
						{
							return VertexElements[i].DataType;
						}
					}
				}
				return D3DDECLTYPE.UBYTE4N;
			}
		}

		// Token: 0x060002D8 RID: 728 RVA: 0x0003C4F4 File Offset: 0x0003A6F4
		private Rx3SimpleMesh[] UpdateRx3SimpleMeshes(Rx3SimpleMesh[] Rx3SimpleMeshes_in)
		{
			checked
			{
				Rx3SimpleMesh[] Rx3SimpleMeshes_out = new Rx3SimpleMesh[Rx3SimpleMeshes_in.Length - 1 + 1];
				int num = Rx3SimpleMeshes_out.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					long b_in = (long)(unchecked((ulong)this.Id_in[b]));
					Rx3SimpleMeshes_out[b] = Rx3SimpleMeshes_in[(int)b_in];
				}
				return Rx3SimpleMeshes_out;
			}
		}

		// Token: 0x060002D9 RID: 729 RVA: 0x0003C53C File Offset: 0x0003A73C
		private Rx3SimpleMesh[] UpdateRx3SimpleMeshes(EA_FxShader_FxRenderableSimple[] RW4Shader_in)
		{
			checked
			{
				Rx3SimpleMesh[] Rx3SimpleMeshes_out = new Rx3SimpleMesh[RW4Shader_in.Length - 1 + 1];
				int num = Rx3SimpleMeshes_out.Length - 1;
				for (int b = 0; b <= num; b++)
				{
					long b_in = (long)(unchecked((ulong)this.Id_in[b]));
					Rx3SimpleMeshes_out[b] = new Rx3SimpleMesh
					{
						PrimitiveType = RW4Shader_in[(int)b_in].PrimitiveType,
						Unknown_1 = 0,
						Unknown_2 = 0,
						Unknown_3 = 0,
						Padding = new uint[2]
					};
				}
				return Rx3SimpleMeshes_out;
			}
		}

		// Token: 0x060002DA RID: 730 RVA: 0x0003C5C0 File Offset: 0x0003A7C0
		private Rx3EdgeMesh[] UpdateRx3EdgeMeshes(Rx3EdgeMesh[] Rx3EdgeMeshes_in, Rx3EdgeMesh[] Rx3EdgeMeshes_out)
		{
			bool flag = Rx3EdgeMeshes_in != null;
			checked
			{
				if (flag)
				{
					Rx3EdgeMeshes_out = Rx3EdgeMeshes_in;
				}
				else
				{
					int num = Rx3EdgeMeshes_out.Length - 1;
					for (int i = 0; i <= num; i++)
					{
						Rx3EdgeMeshes_out[i].Unknown_1 = 0U;
						Rx3EdgeMeshes_out[i].Unknown_2 = 0U;
						Rx3EdgeMeshes_out[i].Unknown_3 = 0U;
						Rx3EdgeMeshes_out[i].Data = new byte[(int)(unchecked((ulong)Rx3EdgeMeshes_out[i].TotalSize) - 16UL - 1UL) + 1];
					}
				}
				return Rx3EdgeMeshes_out;
			}
		}

		// Token: 0x060002DB RID: 731 RVA: 0x0003C634 File Offset: 0x0003A834
		private Rx3AnimationSkin[] Fix_NumRx3AnimationSkins(Rx3AnimationSkin[] Rx3AnimationSkins_out, int NumAnimationSkins)
		{
			bool flag = Rx3AnimationSkins_out.Length != NumAnimationSkins;
			checked
			{
				if (flag)
				{
					int StartIndex = Rx3AnimationSkins_out.Length - 1;
					Rx3AnimationSkins_out = (Rx3AnimationSkin[])Utils.CopyArray(Rx3AnimationSkins_out, new Rx3AnimationSkin[NumAnimationSkins - 1 + 1]);
					bool flag2 = StartIndex + 1 <= Rx3AnimationSkins_out.Length - 1;
					if (flag2)
					{
						int num = StartIndex + 1;
						int num2 = Rx3AnimationSkins_out.Length - 1;
						for (int b = num; b <= num2; b++)
						{
							Rx3AnimationSkins_out[b] = Rx3AnimationSkins_out[StartIndex];
						}
					}
				}
				return Rx3AnimationSkins_out;
			}
		}

		// Token: 0x060002DC RID: 732 RVA: 0x0003C6AC File Offset: 0x0003A8AC
		private Rx3VertexFormat[] Fix_NumRx3VertexFormats(Rx3VertexFormat[] Rx3VertexFormats_out, int NumVertexFormats)
		{
			bool flag = Rx3VertexFormats_out.Length != NumVertexFormats;
			checked
			{
				if (flag)
				{
					int StartIndex = Rx3VertexFormats_out.Length - 1;
					Rx3VertexFormats_out = (Rx3VertexFormat[])Utils.CopyArray(Rx3VertexFormats_out, new Rx3VertexFormat[NumVertexFormats - 1 + 1]);
					bool flag2 = StartIndex + 1 <= Rx3VertexFormats_out.Length - 1;
					if (flag2)
					{
						int num = StartIndex + 1;
						int num2 = Rx3VertexFormats_out.Length - 1;
						for (int b = num; b <= num2; b++)
						{
							Rx3VertexFormats_out[b] = Rx3VertexFormats_out[StartIndex];
						}
					}
				}
				return Rx3VertexFormats_out;
			}
		}

		// Token: 0x04000125 RID: 293
		private string m_FileName;

		// Token: 0x04000126 RID: 294
		private uint[] Id_in;

		// Token: 0x04000127 RID: 295
		private General.EGameType m_GameType_in;

		// Token: 0x04000128 RID: 296
		private General.EGameType m_GameType_out;

		// Token: 0x04000129 RID: 297
		private General.EFileType m_FileType;

		// Token: 0x0400012A RID: 298
		private General.EFileFormat m_FileFormat_in;

		// Token: 0x0400012B RID: 299
		private General.EFileFormat m_FileFormat_out;

		// Token: 0x0400012C RID: 300
		private bool ChkUpdateVFormat;

		// Token: 0x0400012D RID: 301
		private bool ChkUpdateNamesTable;

		// Token: 0x0400012E RID: 302
		private bool ChkMoveScale;

		// Token: 0x0400012F RID: 303
		private ConvertBones m_ConvertBones;
	}
}
